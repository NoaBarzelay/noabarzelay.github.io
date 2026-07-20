# Precept: design decisions

Precept is my personal, self-improving platform for agentic AI processes and data cataloging. It runs locally, learns from my Claude Code sessions, and turns what I correct into typed, reviewable artifacts: rules, conventions, knowledge notes, and eventually skills and agent personas. Deterministic enforcement is one capability inside that, the sharpest edge, not the whole product. This page is the reasoning: the problem I actually hit, the decisions that shaped the build, the alternatives I rejected, and what is honestly not built yet.

## The problem I actually hit

Claude Code is my primary development agent, and working with it produces things worth keeping: corrections, procedures, preferences, the knowledge my work operates on. Almost none of it survives. Chat history is discarded per session, and memory files accrete into a single document that is loaded whole and followed at the model’s discretion. Anthropic’s own docs describe learned preferences as context, not enforced configuration, with roughly 70% compliance. In practice that meant repeating the same corrections week after week: use pnpm not npm, run the tests before saying it works, don’t leave stub code. The corrections evaporated, and nothing in the loop got better.

Precept’s answer is a pipeline. At session end a small model reads the transcript and extracts a candidate lesson, only from turns I actually typed, and abstains by default. The lesson compiles into a typed entity with a defined commit target. Then I review it: `precept keep` or `precept delete`, and nothing takes effect until I keep it. That human gate is the credibility core of the whole system. A tool that silently mints rules from a noisy classifier destroys its own catalog.

## HARD versus SOFT, and what I refuse to claim

Most of what any agent memory layer writes is steering. A convention in a rules file, a skill, a persona’s system prompt: the model reads it and usually follows it. That is the 70% problem, and no phrasing fixes it, because context is guidance, not commands.

So every artifact in Precept carries a tier. HARD means Claude Code mechanically enforces it, independent of what the model feels like doing. Only three surfaces qualify: hooks (a blocked tool call is blocked), permission deny rules, and subagent tool allowlists (a research persona literally cannot edit files). Everything else, which is most of the catalog, is labeled SOFT: it steers, with no compliance guarantee. Precept only ever claims enforcement for the HARD tier, and the boundary is validated in the type system, so an entity cannot claim enforcement it cannot deliver.

The rejected alternative was the one every pitch wants: call the whole thing enforcement. It reads better and it is false. The honest version costs me the bigger headline and buys a number I can defend, which turned out to be the more useful trade in every conversation about this project.

One asymmetry follows from the same logic. The learning loop fails closed: on any error it mints nothing, because a junk rule is worse than a missed one. The enforcement runtime fails open: no bug of mine, missing key, or unreadable cache ever blocks a session, because a tool that breaks your work gets uninstalled.

## How I measure it

Two tiers, answering different questions.

Tier 1 is the deterministic scorecard. `precept evals` runs the real enforcement engine over a committed golden set of 25 cases and tallies a confusion matrix: violations blocked, compliant calls allowed. No model call, no variance, CI-gated on every push. It currently reads 100% recall and a 0% false-block rate, and the claim is bounded on purpose: of the violations it has a rule for, it blocks all of them and blocks nothing compliant.

The metric underneath is the decision I would defend hardest. I score corrected-behavior rate, not block rate. Block count is easy to inflate; an over-broad matcher blocks constantly and looks productive while making the tool unusable. What I actually want to know is whether the agent’s behavior ends up matching the correction, so the false-block column counts as much as the recall column.

Tier 2 asks the harder question: does enforcement change live agent behavior? That has to be a paired before/after with a 95% confidence interval, because infrastructure noise alone shifts agentic eval scores by several points between identical runs, and a single before/after delta is noise dressed as a result. The reporting harness is built; wiring it to live sessions is the next milestone, and the deterministic number stays the headline until the error bars exist.

## Four decisions, with what I rejected

**Keyword-first recall, embeddings behind an eval.** Knowledge notes are retrieved with SQLite FTS5, BM25 ranking, and tag filtering. The rejected default was a vector database from day one, which is what every 2026 starter template reaches for. Rule cards and knowledge notes are terse and jargon-dense, exactly the regime where single-vector embeddings often underperform plain keyword search. So embeddings are gated on a measurement: sqlite-vec gets added only if a Recall@k eval on real queries shows keyword search actually missing on this corpus. Deferred behind a condition, not skipped.

**Grounded composite confidence, not an LLM float.** Every candidate lesson carries a confidence score, and the obvious implementation is asking the model for one. I rejected it because verbalized model confidence is miscalibrated; it clusters near the top regardless of correctness, which makes it decoration. Precept’s confidence is a composite of signals I can verify: is a verbatim quote from my correction present, is the language imperative, is the rule deterministic by construction, did I keep it, does it actually fire over time. Each input is checkable, so the score means something.

**Markdown source of truth, disposable index.** Everything durable is a plain markdown card with YAML frontmatter: diffable, greppable, and version-controlled, so git is the audit log. The SQLite index and the compiled policy cache are derived artifacts on local disk, kept out of any cloud-synced folder because SQLite corrupts under file sync (SQLite documents this itself). The rejected alternative was the database as the primary store, which is faster to build and quietly makes your own data illegible to you. `precept reindex` rebuilds everything from markdown, and that command doubles as the executable test of the invariant: if the rebuild ever diverges, the design is broken.

**Scoping out passive inference.** The expansive version of this product watches everything I do and silently infers my preferences. I decided not to build it, and it was a product call rather than a capacity one. Passive preference inference is the most crowded square on the agent-memory board, and even well-resourced attempts report accuracy nowhere near something you could act on automatically. More important, it is structurally at odds with enforcement: I cannot legitimately hard-block a session on a preference I never stated, and one wrong inferred block would cost more trust than a hundred correct ones earn back. So Precept mints only from explicit corrections in my own typed turns, behind a provenance gate, and nothing takes effect without an explicit keep. The interesting part of the vision survives anyway, just with a review step in front of it.

## What is not built yet

Three of the nine entity types are built: Rule, Knowledge note, Convention. The other six (skills, agent personas, output styles, slash commands, MCP config, permission profiles) are designed and ride the same lesson spine and the same keep/veto gate, so each is a bounded addition; I build them in the order the catalog demands, whichever correction type shows up most in real usage. The typed data catalog, projects and domains and people as first-class records rather than freeform notes, is planned but not started. Background learning, where Precept reads external best practices on its own judgment and drafts proposals, is planned and stays behind the same review gate. The Tier 2 live eval is built but not wired, so the honest behavioral delta does not exist yet.

And there is a measurement gap I do not have a good answer for. I can score the accuracy of the corrections that became entities. I cannot yet measure the ones that never did, the misses, and a system that only grades what it caught is grading itself on a curve.

<!--
Sources (figure -> file):
- "roughly 70% compliance" (Anthropic docs on learned preferences as context): Second Brain/Career/Portfolio Projects/Precept Personal Agentic AI Platform.md ("~70% compliance because it's guidance, not commands"; also ~/code/precept/README.md Problem section "no compliance guarantee").
- "25 cases" golden set: ~/code/precept/README.md Measurement section ("committed golden set of 25 cases").
- "100% recall and a 0% false-block rate": ~/code/precept/README.md Measurement section ("recall 100% (10/10), false-block rate 0% (0/15)").
- "95% confidence interval": ~/code/precept/README.md G1 + Measurement Tier 2.
- "shifts agentic eval scores by several points between identical runs": ~/code/precept/README.md Measurement Tier 2 ("infrastructure noise alone shifts scores by several points"); vault file cites ~6pp (Anthropic "Adding Error Bars to Evals").
- "Three of the nine entity types are built": ~/code/precept/README.md Milestones ("3 of 9 entity types") + ROADMAP.md ("Three entity types are shipped (Rule, Knowledge note, Convention)").
- Nine entity types + HARD/SOFT tier per type + "only claims enforcement for the HARD tier": ~/code/precept/docs/ARTIFACTS.md.
- HARD surfaces = hooks, permission deny, subagent tool-scoping: ~/code/precept/DECISIONS.md Enforcement section.
- Fail-closed DETECT / fail-open runtime: ~/code/precept/README.md (pipeline diagram, N1) + DECISIONS.md Pipeline.
- Keyword-first FTS5/BM25, sqlite-vec gated on Recall@k, terse jargon-dense regime: ~/code/precept/DECISIONS.md Knowledge recall + ROADMAP.md Retrieval.
- Grounded composite confidence signals (quote present, imperative, deterministic, kept, fires) + miscalibrated verbalized confidence: ~/code/precept/DECISIONS.md Pipeline + vault file 2026-06-26 hardening decision 2.
- Markdown source of truth, derived local SQLite, cloud-sync corruption (SQLite howtocorrupt), reindex as executable test: ~/code/precept/DECISIONS.md Storage + vault file STORAGE SAFETY.
- Passive-inference scope-out reasoning (crowded, structurally at odds with hard-blocking, provenance gate, explicit keep): vault file ORIGINAL ANALYSIS 2026-06-23 + 2026-06-26 sections; accuracy figures deliberately omitted from prose.
- Tier 2 harness built / live wiring pending: ~/code/precept/README.md Measurement + ROADMAP.md Coverage and measurement.
- Corrected-behavior rate not block rate: vault file evals section + DECISIONS.md Evals.
- Typed data catalog planned (R2.3), background learning planned (R3.4): ~/code/precept/README.md.
- Coverage gap (measuring misses): ~/code/precept/README.md Open questions.
- Build order set by catalog demand: ~/code/precept/ROADMAP.md ("The catalog is the demand signal").
-->
