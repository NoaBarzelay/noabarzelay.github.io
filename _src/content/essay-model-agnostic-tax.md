Reading a cached prompt on Anthropic's API costs one tenth of the base input price. Writing that same cache costs 1.25 times the base price for the five-minute version, and twice the base price for the one-hour version. So the gap between a cache you get to reuse and a cache you have to rebuild is about 12.5x on the input side. That one number is the whole argument.

A prompt cache is the provider storing the internal state it already computed from the front of your prompt, the part that repeats turn after turn, so it does not have to recompute it on the next request. A token is the unit both the model and the bill are counted in, roughly a few characters of text. The cached state lives on the provider's own machines. It is not a file you hold or move. When you send the next request to a different provider, there is nothing there to read, so you pay to write the whole thing again from scratch.

The comfortable story right now is that models are commoditizing. Sticker prices are converging at the frontier: as of July 2026, GPT-5.5 runs $5 per million input tokens and $30 per million output, Claude Opus 4.8 is $5 and $25, Gemini 3.1 Pro is $2 and $12. Capability is converging alongside price. The advice that follows is to stay model-agnostic: put a gateway in front of every provider, which means a single routing layer that speaks to all of them behind one API key, and send each request to whichever model is cheapest or fastest that week. Lock-in dies, and you get to treat frontier intelligence as an interchangeable commodity.

Capability convergence and sticker convergence are both real. Effective pricing power convergence is not, because the switching cost did not disappear when the sticker prices met. It moved inside the token stream, and it is scoped to whichever provider is currently holding your state.

## The switching cost moved inside the token stream

The old lock-in was in the code. You wrote to one provider's SDK, its function-calling format, its quirks, and swapping meant a rewrite. Gateways genuinely solved that. Vercel's AI Gateway, generally available in 2026, lets you name a model as a plain string like `anthropic/claude-opus-4.8` or `openai/gpt-5.5` and change providers in one line, and with bring-your-own-key support leaving is a base-URL change rather than a rewrite. That part of the promise is delivered.

But the request shape is not where the cost sits anymore. Two kinds of state now accumulate on the provider side and never leave it.

The first is the prompt cache above. It is provider-scoped by construction, because it is computed state sitting on the GPUs that produced it. There is no format in which one provider's cache is readable by another. You cannot warm Opus with a cache OpenAI wrote.

The second is server-side session state. OpenAI's Responses API keeps the model's reasoning trace on its own backend and lets you reference it by a `previous_response_id` instead of resending it. If you turn statefulness off, the alternative it offers is an encrypted reasoning blob that only OpenAI can decrypt, decrypted in memory for the next call and discarded. Either way the working state of a multi-step agent is OpenAI-bound. It is not something a gateway can pick up and hand to Gemini for the next turn.

So the gateway standardizes the request and the response envelope, which is the cheap, portable part, and leaves the expensive, growing part exactly where it was.

## Why the tax grows with the agent's horizon

None of this would matter much if the state stayed small. It does not, because the workloads are getting longer.

METR measures a "task horizon," the length of task a model can complete on its own at a 50% success rate. As of February 2026, Claude Opus 4.6 sat at a 50% time horizon of about 14.5 hours, up from minutes eighteen months earlier, and the doubling interval has compressed to roughly every four to four and a half months since 2023. Longer horizons mean bigger contexts that get re-read across more turns. Every switch to a new provider throws away a warmer, larger cache and forces a full rewrite. The per-switch penalty scales with the size of the cached prefix, and the prefix scales with how long the agent runs.

The clearest evidence that provider-side cache economics, not raw token counts, drive the bill came without anyone switching providers at all. In early March 2026 Anthropic quietly changed the default cache lifetime for Claude Code from one hour back to five minutes. One user's analysis across 119,866 API calls found 17.1% of spend wasted against the one-hour baseline, and 25.9% wasted in March alone, because any pause longer than five minutes expired the cache and the next turn re-uploaded the context at the write rate instead of the read rate. People hit their five-hour quota ceilings for the first time. A single-parameter change to how long the provider keeps its own cache moved real money, in one direction, at the provider's discretion. That is what pricing power looks like when it does not converge.

## The gateway sells the request, and keeps the state

The gateways themselves concede the point in the shape of their own features. OpenRouter added sticky routing: it hashes the opening messages of a conversation, or takes an explicit `session_id`, and pins every following request in that conversation to the same provider. It says plainly that caches cannot be reused across providers, and that sticky routing exists to keep you on one provider so the cache stays warm.

Read that in order. The layer whose entire pitch is that you are not tied to any one provider ships a mechanism whose job is to tie each session to one provider. Sticky routing is the tell. The agnostic layer's own answer to the cache problem is to stop being agnostic for the duration of the work that matters.

## The strongest objection, and where it holds

The honest counterargument is that the tax is bounded, for three reasons, and each one is correct.

Sticky per-session routing means you only pay the switch cost between sessions, not inside them, so short interactions barely feel it. Output tokens, the model's generated text, are never cached and cost the same on every provider, and on long runs output volume is large, so the portable-versus-not question only touches part of the bill. And the price spread that actually matters is not between frontier equals, it is across tiers: Gemini 3.1 Flash-Lite at $0.10 input and $0.40 output sits about 50x below Opus on input, so the real savings in being model-agnostic come from dropping to a cheaper tier for easy calls, not from hedging between two frontier models that cost nearly the same.

All three are right, and together they scope the claim rather than break it. Look at what each one assumes. Tiering down is substituting a weaker model for an easier task, which is a capability decision, not a hedge between equivalent frontier models, and it is the equivalence that the convergence story said was now safe to exploit. Output dilution does bound the share, but agent loops re-read a growing context on every turn, so cached-read volume compounds with turn count precisely in the long-horizon workloads, which are the ones the whole field is racing toward. And the bound from sticky routing is itself the switching cost: to keep the dollar cost bounded you pin the session to one provider, so you pay in lost flexibility instead. The cost did not vanish. It changed denomination.

So the version I would actually defend is narrow. Agnosticism as tiering and as failover, routing to a cheaper model for simple work and to a backup when a provider is down, works and is worth building. Gateways are not dead, and I am not claiming a flat multiple applies to every workload. What quietly stopped working is agnosticism as a frontier hedge, the specific promise that because Opus 4.8 and GPT-5.5 cost the same on the sticker you can swap one for the other mid-workload. That is where the cache write and the stranded session state land, and they land harder the longer the agent runs.

Sticker price converged. Capability converged. The residual is the state, and state is the one thing a gateway cannot standardize, because it physically lives on one company's machines and grows with the horizon of the task. That residual is the part of pricing power that is not converging, and it is sitting inside the token stream the gateway was supposed to make fungible.

<!--
CLAIM-TO-SOURCE MAP

1. Anthropic cache read = 0.1x base input; 5-min cache write = 1.25x base input; 1-hour write = 2x base input; write/read gap ~12.5x.
   - https://platform.claude.com/docs/en/build-with-claude/prompt-caching
   - https://openrouter.ai/docs/guides/best-practices/prompt-caching (quotes "1.25x" write and "0.1x" read for Anthropic)

2. July 2026 frontier sticker prices: GPT-5.5 $5 in / $30 out; Claude Opus 4.8 $5 / $25; Gemini 3.1 Pro $2 / $12; Gemini 3.1 Flash-Lite $0.10 / $0.40.
   - https://benchlm.ai/llm-pricing
   - https://www.developersdigest.tech/blog/frontier-model-api-pricing-june-2026
   - https://www.aimagicx.com/blog/llm-api-pricing-comparison-2026

3. Vercel AI Gateway GA 2026; one-line model swap via creator/model strings (anthropic/claude-opus-4.8, openai/gpt-5.5); BYOK; "avoid lock-in"; leaving is a base-URL change.
   - https://vercel.com/blog/ai-gateway-is-now-generally-available
   - https://vercel.com/docs/ai-gateway
   - https://www.developersdigest.tech/blog/vercel-ai-gateway-guide-2026

4. Prompt cache is provider-scoped computed state; cannot be reused across providers.
   - https://openrouter.ai/docs/guides/best-practices/prompt-caching ("Caches cannot be reused across providers")

5. OpenAI Responses API keeps reasoning trace server-side, referenced by previous_response_id; stateless alternative is encrypted reasoning items decryptable only by OpenAI; state is OpenAI-bound.
   - https://www.seangoedecke.com/responses-api/
   - https://developers.openai.com/api/docs/guides/conversation-state
   - https://community.openai.com/t/how-to-use-reasoning-encrypted-content-with-store-false-stateless/1286934

6. METR task horizon: Claude Opus 4.6 ~14.5h 50%-time horizon as of Feb 21, 2026; doubling ~4.3 months (130.8 days) post-2023, ~4 months over 2024-2025.
   - https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/
   - https://theaidigest.org/time-horizons
   - https://agentmarketcap.ai/blog/2026/04/11/new-moores-law-ai-agent-task-horizons-2026

7. March 2026 Claude Code cache TTL regression (default silently 1h -> 5m early March); analysis of 119,866 calls found 17.1% spend wasted overall, 25.9% in March; users hit 5-hour quota ceilings; pause >5 min re-uploads context at write rate vs read rate.
   - https://github.com/anthropics/claude-code/issues/46829

8. OpenAI prompt caching automatic; GPT-5.5 cached input $0.50 vs $5 base = 0.1x cached read.
   - https://openai.com/index/api-prompt-caching/
   - https://benchlm.ai/llm-pricing

9. OpenRouter sticky routing: hashes opening messages or takes explicit session_id to pin a conversation to one provider so the cache stays warm; caches not shared across providers.
   - https://openrouter.ai/docs/guides/best-practices/prompt-caching
-->
