#!/usr/bin/env python3
"""Generator for the cyber-tech variant: index + 2 essays + 2 decision pages + shared css.
Personal-site backbone: the hero H1 is Noa's NAME; the tagline is the subhead."""
import html, re, pathlib

ROOT = pathlib.Path("/private/tmp/claude-502/-Users-noabarzelay/c749ac7a-cd54-459e-8006-33213de10a5d/scratchpad/redesign-wt")
CONTENT = ROOT / "_content"
OUT = ROOT / "variants" / "cyber"
(OUT / "writing").mkdir(parents=True, exist_ok=True)
(OUT / "notes").mkdir(parents=True, exist_ok=True)

FONTS = ("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700"
         "&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap")
FAVICON = ("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20100%20100'%3E"
           "%3Crect%20width='100'%20height='100'%20rx='24'%20fill='%23070810'/%3E"
           "%3Cdefs%3E%3ClinearGradient%20id='g'%20x1='0'%20y1='0'%20x2='1'%20y2='1'%3E"
           "%3Cstop%20offset='0'%20stop-color='%236EE7F5'/%3E%3Cstop%20offset='1'%20stop-color='%23C08CFF'/%3E"
           "%3C/linearGradient%3E%3C/defs%3E"
           "%3Ctext%20x='50'%20y='68'%20font-family='monospace'%20font-size='46'%20font-weight='700'%20"
           "text-anchor='middle'%20fill='url(%23g)'%3ENB%3C/text%3E%3C/svg%3E")

def inline(t):
    o = html.escape(t, quote=False)
    o = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", o, flags=re.S)
    o = re.sub(r"`([^`]+)`", r"<code>\1</code>", o)
    return o

def md_to_body(md):
    comments = re.findall(r"<!--.*?-->", md, flags=re.S)
    md_wo = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    title, parts = "", []
    for block in re.split(r"\n\s*\n", md_wo.strip()):
        block = block.strip()
        if not block:
            continue
        if block.startswith("# "):
            title = block[2:].strip()
        elif block.startswith("## "):
            parts.append(f'      <h2>{inline(block[3:].strip())}</h2>')
        else:
            parts.append(f"      <p>{inline(block)}</p>")
    body = "\n".join(parts)
    if comments:
        body += "\n" + "\n".join(comments)
    return title, body

HEAD = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{ogtitle}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="{ogtype}">
  <meta property="og:site_name" content="Noa Barzelay">
  <meta name="author" content="Noa Barzelay">
  <link rel="icon" href="{favicon}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{fonts}" rel="stylesheet">
  <link rel="stylesheet" href="{css}">
</head>"""

def head(title, desc, ogtitle, ogtype, css):
    return HEAD.format(title=html.escape(title), desc=html.escape(desc, quote=True),
                       ogtitle=html.escape(ogtitle, quote=True), ogtype=ogtype,
                       favicon=FAVICON, fonts=FONTS, css=css)

BG = """  <div class="bg" aria-hidden="true">
    <div class="bg-grid"></div>
    <div class="bg-glow bg-glow-1"></div>
    <div class="bg-glow bg-glow-2"></div>
    <div class="bg-vignette"></div>
  </div>"""

def nav(prefix=""):
    return f"""  <header class="nav">
    <nav class="nav-links" aria-label="Sections">
      <a href="{prefix}index.html#projects">Projects</a>
      <a href="{prefix}index.html#writing">Writing</a>
      <a href="{prefix}index.html#education">Education</a>
      <a href="{prefix}index.html#experience">Experience</a>
      <a href="{prefix}index.html#interests">Other Interests</a>
    </nav>
  </header>"""

HERO_SVG = """      <svg class="fanout" viewBox="0 0 420 300" fill="none" aria-hidden="true">
        <defs>
          <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stop-color="#6EE7F5" stop-opacity="0.1"/>
            <stop offset="0.5" stop-color="#8B9CFF" stop-opacity="0.9"/>
            <stop offset="1" stop-color="#C08CFF" stop-opacity="0.5"/>
          </linearGradient>
          <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
            <feGaussianBlur stdDeviation="3.2" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>
        <g filter="url(#glow)" stroke="url(#line)" stroke-width="1.4">
          <path d="M40 150 C 150 150, 180 44, 300 44"/>
          <path d="M40 150 C 150 150, 180 97, 300 97"/>
          <path d="M40 150 C 150 150, 190 150, 300 150"/>
          <path d="M40 150 C 150 150, 180 203, 300 203"/>
          <path d="M40 150 C 150 150, 180 256, 300 256"/>
          <path d="M300 44 C 350 44, 350 150, 388 150"/>
          <path d="M300 97 C 348 97, 350 150, 388 150"/>
          <path d="M300 150 L 388 150"/>
          <path d="M300 203 C 348 203, 350 150, 388 150"/>
          <path d="M300 256 C 350 256, 350 150, 388 150"/>
        </g>
        <g class="nodes">
          <circle cx="40" cy="150" r="5.5" class="node node-src"/>
          <circle cx="300" cy="44" r="4" class="node"/>
          <circle cx="300" cy="97" r="4" class="node"/>
          <circle cx="300" cy="150" r="4" class="node"/>
          <circle cx="300" cy="203" r="4" class="node"/>
          <circle cx="300" cy="256" r="4" class="node"/>
          <circle cx="388" cy="150" r="5.5" class="node node-out"/>
        </g>
      </svg>"""

def index_page():
    body = f"""<body>
{BG}
{nav()}
  <main id="main">

    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow"><span class="tick"></span>TECHNICAL PRODUCT MANAGER</p>
        <h1 class="hero-name">Noa <span class="grad">Barzelay</span></h1>
        <p class="hero-title">I'm passionate about turning what AI makes possible into innovative products that make a difference.</p>
        <p class="hero-body">Technical PM spanning hyperscale engineering, growth ownership, and market insight. Built the ML platform at <a href="https://www.microsoft.com/en-us/security/business/endpoint-security/microsoft-defender-endpoint" target="_blank" rel="noopener noreferrer">Microsoft</a>, owned a predictive-AI product through a $300M exit at <a href="https://www.wenrix.com" target="_blank" rel="noopener noreferrer">Wenrix</a>, now venture-capital investing in AI infrastructure, enterprise, and security at <a href="https://www.antler.co" target="_blank" rel="noopener noreferrer">Antler</a>.</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="../../resume/Noa-Barzelay-Resume.pdf" download="Noa Barzelay - Resume.pdf">Resume <span aria-hidden="true">&darr;</span></a>
          <a class="btn" href="https://linkedin.com/in/noa-barzelay" target="_blank" rel="noopener noreferrer">LinkedIn <span class="ext" aria-hidden="true">&#8599;</span></a>
          <a class="btn" href="mailto:noabarzelay@gmail.com">Email</a>
        </div>
      </div>
      <div class="hero-visual">
{HERO_SVG}
      </div>
    </section>

    <section id="projects" class="block">
      <div class="block-head">
        <span class="idx">01</span><h2 class="block-title">Projects</h2><span class="rule"></span>
      </div>
      <div class="cards">

        <article class="card">
          <div class="card-top">
            <h3>Precept</h3>
            <div class="taglist"><span class="pill">Python</span><span class="pill">Claude Code</span><span class="pill">Evals</span></div>
          </div>
          <p>Precept is my personal, self-improving platform for agentic AI processes and data cataloging. It continuously learns from my sessions to improve its data catalog, its defined entities (rules, skills, agent personas, and more), and its processes, both through explicit direction and background learning.</p>
          <div class="card-links">
            <a href="https://github.com/NoaBarzelay/precept" target="_blank" rel="noopener noreferrer">GitHub <span class="ext" aria-hidden="true">&#8599;</span></a>
            <a href="notes/precept.html">Design decisions <span aria-hidden="true">&rarr;</span></a>
          </div>
        </article>

        <article class="card">
          <div class="card-top">
            <h3>Thesis Engine</h3>
            <div class="taglist"><span class="pill">TypeScript</span><span class="pill">Multi-agent</span><span class="pill status">In development</span></div>
          </div>
          <p>Thesis Engine is my multi-agent research engine for venture capital investment theses and deal sourcing. It takes a thesis broad idea, writes a falsifiable litmus test, decomposes the market into solution-oriented categories, and outputs a sourced report with a ranked list of potential investments.</p>
          <p>The pipeline begins with a planner that writes the litmus test, a falsifiable rule for what qualifies as a fit, and I review and edit it before any research runs. Parallel agents then research each category, an adversarial critic deduplicates companies across categories and flags thin evidence, and a scoring stage ranks what survives against my investment criteria. A deterministic eval harness runs in CI on every push.</p>
          <div class="card-links">
            <a href="notes/thesis-engine.html">Design decisions <span aria-hidden="true">&rarr;</span></a>
          </div>
        </article>

      </div>
    </section>

    <section id="writing" class="block">
      <div class="block-head">
        <span class="idx">02</span><h2 class="block-title">Writing</h2><span class="rule"></span>
      </div>
      <ul class="writing-list">
        <li><a href="writing/layer-beneath.html">
          <div class="w-main"><span class="w-kind">ESSAY</span><span class="w-title">The Layer Beneath the Agents</span></div>
          <p class="w-prev">A 45-product map of the coding-agent orchestrator market, and why the durable companies get built in the neutral cross-vendor governance, cost, and audit layer beneath the agents.</p>
        </a></li>
        <li><a href="writing/agentic-security.html">
          <div class="w-main"><span class="w-kind">ESSAY</span><span class="w-title">Agents Broke the Security Stack</span></div>
          <p class="w-prev">Prompt injection is social engineering, not SQL injection, so it will never be patched away, and the durable money in agent security sits in the boring containment and identity layers.</p>
        </a></li>
        <li><a href="notes/precept.html">
          <div class="w-main"><span class="w-kind">NOTES</span><span class="w-title">Precept: design decisions</span></div>
          <p class="w-prev">Why I only claim enforcement for the deterministic subset, the eval that keeps that claim honest, and four decisions where I rejected the default.</p>
        </a></li>
        <li><a href="notes/thesis-engine.html">
          <div class="w-main"><span class="w-kind">NOTES</span><span class="w-title">Thesis Engine: five decisions and what they replaced</span></div>
          <p class="w-prev">Owning the orchestration loop, sealing bring-your-own keys, failing loud but finishing, fixing the output schema, and gating merges on evals.</p>
        </a></li>
      </ul>
    </section>

        <section id="education" class="block">
      <div class="block-head">
        <span class="idx">03</span><h2 class="block-title">Education</h2><span class="rule"></span>
      </div>
      <div class="timeline">
        <div class="exp">
          <div class="exp-yr">2025-2026<span class="exp-loc">New York, NY</span></div>
          <div class="exp-body">
            <h3>MBA <span class="org">Columbia Business School</span></h3>
            <ul class="exp-bullets">
              <li>GMAT Score: 780 (99th percentile).</li>
              <li>Honors: Dean's List (9.63/10 GPA); merit-based scholarship, 65% of tuition.</li>
              <li>Extracurricular: AI Club, Tech Club, VC Club, Entrepreneurship Club Vice President.</li>
            </ul>
          </div>
        </div>
        <div class="exp">
          <div class="exp-yr">2018-2022<span class="exp-loc">Tel Aviv, IL</span></div>
          <div class="exp-body">
            <h3>BS, Computer Science &amp; Economics (Double Major) <span class="org">Tel Aviv University</span></h3>
            <ul class="exp-bullets">
              <li>Honors: Magna Cum Laude in Economics (95th percentile); Academic Excellence Scholarship.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section id="experience" class="block">
      <div class="block-head">
        <span class="idx">04</span><h2 class="block-title">Experience</h2><span class="rule"></span>
      </div>

      <div class="exp-group">Product &amp; Engineering</div>
      <div class="timeline">
        <div class="exp">
          <div class="exp-yr">2023-2025<span class="exp-loc">Tel Aviv, IL</span></div>
          <div class="exp-body">
            <h3>Product Manager <span class="org">Wenrix</span></h3>
            <p class="exp-context">Enterprise predictive-AI platform for flight pricing optimization, powering 60+ Online Travel Agencies. Acquired by Etraveli for $300M (12/2025).</p>
            <ul class="exp-bullets">
              <li>Owned Wenrix's core predictive-pricing platform (~60% of company revenue); drove roadmap through R&amp;D and GTM to +$2M annual revenue increase (10%) in 10 months via usage and margin expansion.</li>
              <li>Led cross-functional team of 15 engineers, researchers and sales in launching two new products, from customer discovery to activation and monetization utilizing A/B-tested rollouts; +$2.5M ARR (12% of company revenue) in 6 months.</li>
              <li>Drove enterprise adoption, including nine strategic contracts, owning product engagements with enterprise executives on needs and outcomes, technical integration (APIs, custom builds) and quality, security and cost trade-offs.</li>
              <li>Ideated and launched AI automation + infra platform to cut new-customer time-to-value 30% with roadmap to self-serve offering unlocking the long-tail market (~3x revenue potential).</li>
            </ul>
          </div>
        </div>
        <div class="exp">
          <div class="exp-yr">2020-2023<span class="exp-loc">Herzliya, IL</span></div>
          <div class="exp-body">
            <h3>Software Engineer &rarr; Software Engineer II <span class="org">Microsoft</span></h3>
            <p class="exp-context">Microsoft Defender for Endpoint (protecting 500M+ devices, monitoring 10T+ events/day). Fast-tracked to SWE II in 11 months.</p>
            <ul class="exp-bullets">
              <li>Owned core ML-based detection services and KPIs, re-architecting the platform for hyperscale, migrating it to Kubernetes with zero-data-loss cutover and cutting production errors from thousands per hour to tens.</li>
              <li>Initiated and led 4 engineers in building a CI/CD platform validating and automatically mitigating platform quality regressions, improving DORA metrics; now the safety standard across three engineering groups.</li>
              <li>Built a self-serve researcher/developer platform to ship new cybersecurity ML logic, cutting time-to-protection against emerging threats from months to hours; widely adopted.</li>
              <li>Cut platform compute up to 30% ($3M/yr) and sped core processing up to ~5x through re-prioritizing detection workloads by impact, algorithmic optimization, and demand-based autoscaling.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="exp-group">Tech Investing</div>
      <div class="timeline">
        <div class="exp">
          <div class="exp-yr">2026-Present<span class="exp-loc">New York, NY</span></div>
          <div class="exp-body">
            <h3>MBA Investment Associate <span class="org">Antler</span></h3>
            <p class="exp-context">Global venture capital fund; $1.5B AUM; 1500+ investments.</p>
            <ul class="exp-bullets">
              <li>Source and lead deals driven by authored technical investment theses on how AI reshapes enterprise software, infrastructure, and security (including agentic-AI security, computer-use agents, GPU/TPU neoclouds).</li>
              <li>Build and own a multi-agent research and deal-sourcing platform used across the investment team.</li>
            </ul>
          </div>
        </div>
        <div class="exp">
          <div class="exp-yr">2025<span class="exp-loc">New York, NY</span></div>
          <div class="exp-body">
            <h3>MBA Investment Associate, Founding Member <span class="org">Canopy</span></h3>
            <p class="exp-context">Stealth venture capital fund investing in AI infrastructure.</p>
            <ul class="exp-bullets">
              <li>Identified and evaluated AI infrastructure startups incl. market breakdown, growth trajectory, technical product and roadmap.</li>
              <li>Designed and built an agentic deal-sourcing and evaluation framework, identifying high-potential AI infrastructure ventures.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="exp-group">Israel Defense Forces</div>
      <div class="timeline">
        <div class="exp">
          <div class="exp-yr">2014-2017<span class="exp-loc">Israel</span></div>
          <div class="exp-body">
            <h3>Flight Academy Cadet &rarr; Aerial Operations Officer</h3>
            <ul class="exp-bullets">
              <li>Directed real-time missions of Israeli Air Force aircraft, helicopter, and UAV; led a team of officers and collaborated daily with IAF Generals and with the US Air Force in joint counter-terrorism missions involving 50+ personnel.</li>
              <li>Selected to the elite IAF Pilots Course (~4% admission); reached top-quartile and remained the last woman in the squadron.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
        <section id="interests" class="block">
      <div class="block-head">
        <span class="idx">05</span><h2 class="block-title">Other Interests</h2><span class="rule"></span>
      </div>
      <div class="interests">
        <div class="int-group">
          <h3 class="int-label">Volunteering</h3>
          <ul class="int-list">
            <li>Lectured to and mentored women in STEM through &lsquo;Shavot&rsquo; nonprofit and Microsoft, helping them break into tech and grow in it.</li>
            <li>Analyzed economic policy for Lobby99, a nonpartisan lobby for the Israeli public interest, actually influencing legislation.</li>
            <li>Tutored Hebrew one-on-one to new immigrant women, helping them gain the footing to integrate and find work in Israel.</li>
            <li>Counseled and raised funds for children battling cancer, through Larger Than Life.</li>
            <li>Counseled at-risk youth.</li>
          </ul>
        </div>
        <div class="int-group">
          <h3 class="int-label">Personal</h3>
          <ul class="int-list">
            <li>Danced contemporary for 24 years and competed nationally.</li>
            <li>Currently training for my first half marathon. My Vizsla, Sol, is my unofficial running coach.</li>
            <li>Meditating daily, attending a silent retreat every year.</li>
            <li>Lifelong reader; at ten I broke my local library&rsquo;s annual borrowing record (143). I read both non-fiction and fiction, especially sci-fi and fantasy.</li>
          </ul>
        </div>
      </div>
    </section>

  </main>

  <footer class="foot">
    <div class="foot-row">
      <a href="mailto:noabarzelay@gmail.com">noabarzelay@gmail.com</a>
      <span class="foot-loc">New York, NY / Tel Aviv, IL</span>
    </div>
  </footer>
  <!-- GoatCounter privacy-friendly analytics (free). Register the code "noabarzelay" at https://www.goatcounter.com/ ;
       if that code is taken, pick another and replace it in the URL below (one place per page). -->
  <script data-goatcounter="https://noabarzelay.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>"""
    doc = (head("Noa Barzelay",
                "Noa Barzelay builds agentic AI tooling and invests in early-stage AI infrastructure. Investor at Antler, MBA at Columbia, formerly product at Wenrix and engineering at Microsoft.",
                "Noa Barzelay", "website", "styles.css")
           + "\n" + body + "\n")
    doc = doc.replace("<body>", "<!-- subhead (honest, no lab/research overclaim) options: A1 I'm passionate about turning what AI makes possible into products people trust. | A2 I love turning powerful AI into products people can trust. | A3 I love turning complex technology into products people rely on. | A4 I love building products on top of powerful AI, the kind people actually trust. -->\n<body>", 1)
    (OUT / "index.html").write_text(doc, encoding="utf-8")
    print("wrote index.html")

def article_page(md_file, out_rel, kind, meta_extra, desc):
    md = (CONTENT / md_file).read_text(encoding="utf-8")
    title, body = md_to_body(md)
    doc = head(f"{title} | Noa Barzelay", desc, title, "article", "../styles.css")
    doc += f"""
<body class="reading">
{BG}
{nav("../")}
  <main id="main">
    <article class="article">
      <p class="crumb"><a href="../index.html">&larr; Noa Barzelay</a> <span class="crumb-sep">/</span> <span>{html.escape(kind)}</span></p>
      <div class="article-eyebrow"><span class="w-kind">{html.escape(kind.upper())}</span><span class="dotsep">&middot;</span><span>{html.escape(meta_extra)}</span></div>
      <h1 class="article-title">{html.escape(title)}</h1>
      <p class="article-stand">{html.escape(desc)}</p>
      <div class="article-body">
{body}
      </div>
      <footer class="article-foot">
        <a href="../index.html">&larr; Back to index</a>
        <a href="mailto:noabarzelay@gmail.com">noabarzelay@gmail.com</a>
      </footer>
    </article>
  </main>
  <!-- GoatCounter privacy-friendly analytics (free). Register the code "noabarzelay" at https://www.goatcounter.com/ ;
       if that code is taken, pick another and replace it in the URL below (one place per page). -->
  <script data-goatcounter="https://noabarzelay.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""
    (OUT / out_rel).write_text(doc, encoding="utf-8")
    print("wrote", out_rel)

index_page()
article_page("essay-layer-beneath.md", "writing/layer-beneath.html", "Essay", "April 2026",
             "A 45-product map of the coding-agent orchestrator market, and why the durable companies get built in the neutral cross-vendor governance, cost, and audit layer beneath the agents.")
article_page("essay-agentic-security.md", "writing/agentic-security.html", "Essay", "2026",
             "Prompt injection is social engineering, not SQL injection, so it will never be patched away, and the durable money in agent security sits in the boring containment and identity layers, not the headline firewall category the acquirers have already bought out.")
article_page("precept-decisions.md", "notes/precept.html", "Notes", "Precept",
             "Why I only claim enforcement for the deterministic subset, the eval that keeps that claim honest, and four decisions where I rejected the default.")
article_page("thesis-decisions.md", "notes/thesis-engine.html", "Notes", "Thesis Engine",
             "Owning the orchestration loop, sealing bring-your-own keys, failing loud but finishing, fixing the output schema, and gating merges on evals.")
print("done")
