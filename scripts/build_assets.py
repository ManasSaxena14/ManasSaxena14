#!/usr/bin/env python3
"""Generates the SVGs used by the profile README.

Design language matches the portfolio (manas-saxena.vercel.app): zinc neutrals,
one lime accent, editorial type (sans + italic serif + mono labels) and calm,
play-once motion.

Run:  python3 scripts/build_assets.py      (writes into ./art)
Edit the DATA section below to change text, then re-run.
"""
import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "art")
os.makedirs(OUT, exist_ok=True)

# ---------- palette (mirrors the portfolio's globals.css tokens) ----------
BG = "#09090b"
SURFACE = "#111113"
SURFACE_2 = "#18181b"
LINE = "#27272a"
LINE_SOFT = "#1e1e22"
INK = "#fafafa"
INK_2 = "#e4e4e7"
SOFT = "#c4c4cc"
MUTED = "#a1a1aa"
DIM = "#8b8b94"
FAINT = "#5f5f68"
ACCENT = "#c8f25a"

SANS = "'Inter', 'Geist', 'Helvetica Neue', 'Segoe UI', Helvetica, Arial, sans-serif"
SERIF = "'Instrument Serif', 'Iowan Old Style', Georgia, 'Times New Roman', serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace"

EASE = "cubic-bezier(.2,.8,.2,1)"


def esc(s):
    return escape(s, {'"': "&quot;"})


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name)


def base_css():
    return (f"@keyframes up {{ from {{opacity:0;transform:translateY(8px)}} to {{opacity:1;transform:none}} }}"
            f"@keyframes fade {{ from {{opacity:0}} to {{opacity:1}} }}"
            ""
            f"@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}")


def panel(W, H, rx=16, fill=SURFACE):
    return (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="{rx}" fill="{fill}" stroke="{LINE}"/>')


# =====================================================================
# HEADER
# =====================================================================
def logo_mark(x, y, s=1.0):
    """MS monogram drawn as a circuit trace, ending in a lime node (as on the portfolio)."""
    d = ("M0 34 V6 L11 24 L22 6 V34"            # deep-V M
         " M44 8 H32 L28 12 V18 L32 21 H40 L44 25 V31 L40 34 H28")  # chamfered S
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="square" stroke-linejoin="miter"/>'
            f'<circle cx="28" cy="34" r="3.2" fill="{ACCENT}"/></g>')


def header():
    W, H = 1000, 320
    trace = "M640 186 H730 L748 168 V128 L766 110 H840 L858 92 V70 H930"
    trace2 = "M700 196 H880 L896 180 V140 H972"
    nodes = [(730, 186), (748, 128), (840, 110), (858, 70), (880, 196), (896, 140)]
    node_svg = "".join(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{BG}" stroke="{FAINT}" stroke-width="1.2"/>' for x, y in nodes)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Manas Saxena, Full-Stack and AI Engineer">
<title>Manas Saxena · Full-Stack &amp; AI Engineer</title>
<defs>
  <clipPath id="clip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16"/></clipPath>
  <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#fff" fill-opacity=".06"/></pattern>
  <linearGradient id="fadeR" x1="0" x2="1"><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
  <mask id="dotMask"><rect width="{W}" height="{H}" fill="url(#fadeR)"/></mask>
  <radialGradient id="halo" cx=".86" cy=".2" r=".55"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".07"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
</defs>
<style><![CDATA[
  {base_css()}
  .meta {{ font: 500 11px {MONO}; letter-spacing: 1.6px; fill: {DIM}; }}
  .first {{ font: 700 86px {SANS}; letter-spacing: -3px; fill: {INK}; }}
  .last {{ font: italic 400 92px {SERIF}; letter-spacing: -1px; fill: {INK_2}; }}
  .role {{ font: 500 19px {SANS}; fill: {INK_2}; }}
  .sub {{ font: 400 14px {SANS}; fill: {MUTED}; }}
  .sig {{ offset-path: path("{trace}"); animation: sig 6s 1s ease-in-out infinite; opacity: 0; }}
  .pulse {{ transform-box: fill-box; transform-origin: center; animation: pulse 2.8s ease-out infinite; }}
  @keyframes draw {{ to {{ stroke-dashoffset: 0 }} }}
  @keyframes sig {{ 0% {{offset-distance:0%;opacity:0}} 8% {{opacity:1}} 55% {{offset-distance:100%;opacity:1}} 62%,100% {{offset-distance:100%;opacity:0}} }}
  @keyframes pulse {{ 0% {{transform:scale(1);opacity:.6}} 70%,100% {{transform:scale(3.2);opacity:0}} }}
]]></style>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#dotMask)"/>
  <rect width="{W}" height="{H}" fill="url(#halo)"/>

  <g fill="none" stroke-width="1.4" stroke-linejoin="round">
    <path class="trace" d="{trace2}" stroke="{LINE}" pathLength="1"/>
    <path class="trace" d="{trace}" stroke="#3f3f46" pathLength="1"/>
  </g>
  {node_svg}
  <circle cx="930" cy="70" r="4" fill="{ACCENT}" />
  <circle cx="930" cy="70" r="4" fill="none" stroke="{ACCENT}" class="pulse"/>
  <circle r="2.6" fill="{ACCENT}" class="sig"/>

  <g >{logo_mark(44, 34, .72)}</g>
  <text class="meta" x="88" y="56">MANAS SAXENA <tspan fill="{FAINT}">/</tspan> PORTFOLIO <tspan fill="{FAINT}">/</tspan> 2026</text>
  <g >
    <circle cx="{W - 222}" cy="52" r="3.5" fill="{ACCENT}"/>
    <text class="meta" x="{W - 210}" y="56" fill="{INK_2}" style="fill:{SOFT}">OPEN TO INTERNSHIPS</text>
  </g>

  <text  x="40" y="166"><tspan class="first">Manas</tspan><tspan class="last" dx="18">Saxena</tspan><tspan class="last" style="fill:{ACCENT}">.</tspan></text>

  <text class="role" x="44" y="220">Full-Stack &amp; AI Engineer <tspan fill="{FAINT}">—</tspan> <tspan fill="{MUTED}">shipping systems that are correct, fast and tested.</tspan></text>
  <text class="sub" x="44" y="246">B.Tech CS &amp; AI · Newton School of Technology × Rishihood University · 2024–28</text>

  <line x1="44" y1="274" x2="{W - 44}" y2="274" stroke="{LINE_SOFT}"/>
  <g >
    <text class="meta" x="44" y="298">BASED IN INDIA</text>
    <text class="meta" x="{W / 2}" y="298" text-anchor="middle">LLM SYSTEMS · BACKENDS · DATA</text>
    <text class="meta" x="{W - 44}" y="298" text-anchor="end" style="fill:{SOFT}">MANAS-SAXENA.VERCEL.APP <tspan fill="{ACCENT}">↗</tspan></text>
  </g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{LINE}"/>
</svg>'''
    write("header.svg", svg)


# =====================================================================
# ABOUT (profile sheet)
# =====================================================================
ABOUT_ROWS = [
    ("EDUCATION", "B.Tech Computer Science & AI · Newton School of Technology × Rishihood University · 2024–28"),
    ("I BUILD", "LLM gateways · agentic AI pipelines · race-safe backends · data stories"),
    ("CORE STACK", "TypeScript · Next.js · NestJS · FastAPI · PostgreSQL · Redis · LangGraph"),
    ("I CARE ABOUT", "Concurrency, correctness, test coverage and p95 latency"),
    ("OFF KEYBOARD", "Vice President, Finance Club (FinSetu India–US) · Operations Head, Esports Club"),
    ("OPEN TO", "Internships · collaborations · hard engineering problems"),
]


def about():
    W = 1000
    top = 132
    RH = 44
    H = top + len(ABOUT_ROWS) * RH + 28
    rows = []
    for i, (k, v) in enumerate(ABOUT_ROWS):
        y = top + i * RH
        rows.append(f'''<g >
  <line x1="40" y1="{y}" x2="{W - 40}" y2="{y}" stroke="{LINE_SOFT}"/>
  <text class="k" x="40" y="{y + 27}">{esc(k)}</text>
  <text class="v" x="220" y="{y + 27}">{esc(v)}</text></g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="About Manas Saxena">
<title>About · Manas Saxena</title>
<style><![CDATA[
  {base_css()}
  .lead {{ font: 500 26px {SANS}; letter-spacing: -.4px; fill: {INK}; }}
  .lead2 {{ font: 400 26px {SANS}; letter-spacing: -.4px; fill: {MUTED}; }}
  .it {{ font-family: {SERIF}; font-style: italic; font-weight: 400; font-size: 29px; }}
  .k {{ font: 500 11px {MONO}; letter-spacing: 1.6px; fill: {DIM}; }}
  .v {{ font: 400 15px {SANS}; fill: {INK_2}; }}
]]></style>
{panel(W, H)}
<text class="lead" x="40" y="62">I ship production-grade systems where <tspan class="it" fill="{ACCENT}">correctness</tspan> is measurable —</text>
<text class="lead2" x="40" y="98">race-safe, load-tested and covered by the tests that prove it.</text>
{''.join(rows)}
</svg>'''
    write("about.svg", svg)

# =====================================================================
# STACK (monochrome, replaces the colourful icon grid)
# =====================================================================
STACK = [
    ("LANGUAGES", ["TypeScript", "JavaScript", "Python", "C++", "SQL"]),
    ("FRONTEND", ["Next.js", "React", "Tailwind CSS", "Three.js", "Vite"]),
    ("BACKEND", ["Node.js", "NestJS", "Express", "FastAPI", "Prisma"]),
    ("DATA & CLOUD", ["PostgreSQL", "Redis", "MongoDB", "AWS", "Docker"]),
]
STACK_AI = ["LangGraph", "LangChain", "RAG", "Hugging Face", "scikit-learn", "Pandas", "NumPy", "DuckDB", "Tableau"]


def stack():
    W = 1000
    cw = (W - 80) / 4
    rows = max(len(v) for _, v in STACK)
    top = 40
    col_h = 44 + rows * 30
    ai_y = top + col_h + 30
    H = ai_y + 92
    cols = []
    for i, (k, items) in enumerate(STACK):
        x = 40 + i * cw
        if i:
            cols.append(f'<line x1="{x - 1:.1f}" y1="{top}" x2="{x - 1:.1f}" y2="{top + col_h - 10}" stroke="{LINE_SOFT}"/>')
        pad = 0 if i == 0 else 24
        cols.append(f'<text class="k" x="{x + pad:.1f}" y="{top + 12}">{esc(k)}</text>')
        for j, it in enumerate(items):
            cols.append(f'<text class="v" x="{x + pad:.1f}" y="{top + 48 + j * 30}">{esc(it)}</text>')
    chips, px = [], 40
    for t in STACK_AI:
        w = len(t) * 7.4 + 26
        chips.append(f'<rect x="{px:.1f}" y="{ai_y + 30}" width="{w:.1f}" height="28" rx="14" fill="{SURFACE_2}" stroke="{LINE}"/>'
                     f'<text class="pl" x="{px + w / 2:.1f}" y="{ai_y + 48.5}" text-anchor="middle">{esc(t)}</text>')
        px += w + 8
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack">
<title>Tech stack</title>
<style><![CDATA[
  .k {{ font: 500 11px {MONO}; letter-spacing: 1.6px; fill: {DIM}; }}
  .v {{ font: 400 16px {SANS}; fill: {INK_2}; }}
  .pl {{ font: 500 12px {MONO}; fill: {SOFT}; }}
]]></style>
{panel(W, H)}
{''.join(cols)}
<line x1="40" y1="{ai_y - 8}" x2="{W - 40}" y2="{ai_y - 8}" stroke="{LINE_SOFT}"/>
<text class="k" x="40" y="{ai_y + 16}">AI · ML · DATA</text>
{''.join(chips)}
</svg>'''
    write("stack.svg", svg)


# =====================================================================
# SECTION TITLES
# =====================================================================
def section(slug, idx, label, note):
    W, H = 1000, 64
    lw = len(label) * 15.2 + 8  # approx width of the 26px label
    x_line = 64 + lw + 20
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}">
<title>{esc(label)}</title>
<style><![CDATA[
  {base_css()}
  .idx {{ font: 500 12px {MONO}; letter-spacing: 1.5px; fill: {ACCENT}; }}
  .lbl {{ font: 600 26px {SANS}; letter-spacing: -.5px; fill: {INK}; }}
  .note {{ font: 500 11px {MONO}; letter-spacing: 1.6px; fill: {DIM}; }}
  @keyframes grow {{ from {{transform:scaleX(0)}} to {{transform:scaleX(1)}} }}
]]></style>
<g >
  <text class="idx" x="2" y="41">{esc(idx)}</text>
  <text class="lbl" x="64" y="43">{esc(label)}</text>
</g>
<line class="ln" x1="{x_line:.0f}" y1="34" x2="{W - 24 - len(note) * 8.2:.0f}" y2="34" stroke="{LINE}"/>
<text class="note" x="{W - 2}" y="38" text-anchor="end">{esc(note)}</text>
</svg>'''
    write(f"section_{slug}.svg", svg)


# =====================================================================
# PROJECT CARDS
# =====================================================================
def chip_w(t):
    return len(t) * 6.9 + 22


def card(c):
    W = c.get("W", 500)
    metrics = c["metrics"]
    desc_y = 140
    desc_end = desc_y + (len(c["desc"]) - 1) * 20
    my = desc_end + 30
    py = my + 80 if metrics else desc_end + 28
    H = py + 50

    status = c["status"]
    st_w = len(status) * 7.4 + 30

    desc = "".join(f'<text class="d" x="28" y="{desc_y + i * 20}">{esc(l)}</text>' for i, l in enumerate(c["desc"]))

    mtx = []
    if metrics:
        mw = (W - 56) / len(metrics)
        mtx.append(f'<line x1="28" y1="{my}" x2="{W - 28}" y2="{my}" stroke="{LINE_SOFT}"/>')
        for i, (num, lbl) in enumerate(metrics):
            x = 28 + i * mw
            if i:
                mtx.append(f'<line x1="{x - 1:.1f}" y1="{my + 14}" x2="{x - 1:.1f}" y2="{my + 54}" stroke="{LINE_SOFT}"/>')
            pad = 0 if i == 0 else 18
            mtx.append(f'''<g >
  <text class="mn" x="{x + pad:.1f}" y="{my + 38}">{esc(num)}</text>
  <text class="ml" x="{x + pad:.1f}" y="{my + 56}">{esc(lbl)}</text></g>''')

    chips, px = [], 28
    for t in c["tech"]:
        w = chip_w(t)
        if px + w > W - 28:
            break
        chips.append(f'<rect x="{px:.1f}" y="{py}" width="{w:.1f}" height="24" rx="12" fill="{SURFACE_2}" stroke="{LINE}"/>'
                     f'<text class="pl" x="{px + w / 2:.1f}" y="{py + 16}" text-anchor="middle">{esc(t)}</text>')
        px += w + 8

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(c['title'])}: {esc(c['subtitle'])}">
<title>{esc(c['title'])} · {esc(c['subtitle'])}</title>
<defs>
  <clipPath id="clip-{c['id']}"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16"/></clipPath>
  <radialGradient id="rg-{c['id']}" cx="1" cy="0" r=".75"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".055"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
</defs>
<style><![CDATA[
  {base_css()}
  .idx {{ font: 500 11px {MONO}; letter-spacing: 1.6px; fill: {ACCENT}; }}
  .cat {{ font: 500 11px {MONO}; letter-spacing: 1.6px; fill: {DIM}; }}
  .ti {{ font: 700 30px {SANS}; letter-spacing: -.8px; fill: {INK}; }}
  .st {{ font: italic 400 19px {SERIF}; fill: {SOFT}; }}
  .d {{ font: 400 13.5px {SANS}; fill: {MUTED}; }}
  .mn {{ font: 600 24px {SANS}; letter-spacing: -.5px; fill: {INK}; }}
  .ml {{ font: 500 10.5px {MONO}; letter-spacing: .6px; fill: {DIM}; }}
  .pl {{ font: 500 11px {MONO}; fill: {SOFT}; }}
  .chip {{ font: 500 10.5px {MONO}; letter-spacing: 1.4px; fill: {SOFT}; }}
]]></style>
<g clip-path="url(#clip-{c['id']})">
  <rect width="{W}" height="{H}" fill="{SURFACE}"/>
  <rect width="{W}" height="{H}" fill="url(#rg-{c['id']})"/>
  <g >
    <text class="idx" x="28" y="40">{esc(c['idx'])}</text>
    <text class="cat" x="56" y="40">{esc(c['cat'])}</text>
    <rect x="{W - 28 - st_w:.1f}" y="24" width="{st_w:.1f}" height="24" rx="12" fill="none" stroke="{LINE}"/>
    <circle cx="{W - 28 - st_w + 14:.1f}" cy="36" r="3" fill="{ACCENT}"/>
    <text class="chip" x="{W - 28 - st_w + 23:.1f}" y="40">{esc(status)}</text>
  </g>
  <g >
    <text class="ti" x="27" y="86">{esc(c['title'])}</text>
    <text class="st" x="28" y="{desc_y - 26}">{esc(c['subtitle'])}</text>
  </g>
  <g >{desc}</g>
  {''.join(mtx)}
  <g >{''.join(chips)}</g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{LINE}"/>
</svg>'''
    write(f"card_{c['id']}.svg", svg)


CARDS = [
    dict(id="hireflow", W=1000, status="LIVE", idx="01", cat="FEATURED · HIRING PLATFORM + ATS",
         title="HireFlow", subtitle="A two-sided hiring platform and applicant tracking system",
         desc=["Job seekers track every application; companies post jobs, run their hiring pipeline and book interviews with 4-role RBAC.",
               "Double-booking is impossible via Postgres exclusion constraints (verified at 20 concurrent bookings); resumes scored by TF-IDF."],
         metrics=[("441", "tests in CI"), ("97%", "API coverage"),
                  ("<25ms", "p95 at 50 concurrent users"), ("7", "pg-boss job queues")],
         tech=["Next.js", "NestJS", "PostgreSQL", "pg-boss", "TF-IDF", "RBAC", "Vercel", "Render"]),
    dict(id="finsight", status="LIVE", idx="02", cat="AI FINTECH",
         title="FinSight AI", subtitle="Personal-finance forecasting and advisory",
         desc=["Time-series spend forecasts, overspend risk, anomaly detection",
               "and Monte Carlo goal planning, plus a guarded LLM advisor."],
         metrics=[("RAG", "grounded advisor"), ("PII", "guardrails"), ("CI/CD", "with Docker")],
         tech=["FastAPI", "React", "MongoDB", "scikit-learn", "Docker"]),
    dict(id="bidverse", status="LIVE", idx="03", cat="REAL-TIME MARKETPLACE",
         title="BidVerse", subtitle="A MERN auction marketplace",
         desc=["Race-safe bidding: simultaneous equal bids resolve to one",
               "winner and one HTTP 409. Idempotent bids, auto-settled fees."],
         metrics=[("30+", "REST APIs"), ("16", "pages shipped"), ("6", "Mongo pipelines")],
         tech=["React", "Node.js", "Express", "MongoDB", "Groq AI"]),
    dict(id="churnly", status="LIVE", idx="04", cat="AGENTIC AI",
         title="Churnly", subtitle="Explains why customers churn",
         desc=["A 21-node LangGraph pipeline: survival analysis, corrected stats,",
               "adversarial LLM review and RAG into a cited retention playbook."],
         metrics=[("21", "LangGraph nodes"), ("CoxPH", "+ Kaplan-Meier"), ("CI", "tested pipeline")],
         tech=["LangGraph", "FastAPI", "Next.js", "DuckDB", "RAG"]),
    dict(id="orbyt", status="LIVE", idx="05", cat="LLM INFRASTRUCTURE",
         title="Orbyt", subtitle="A self-hosted, OpenAI-compatible LLM gateway",
         desc=["Drop-in /v1/chat/completions with fallback chains, BYOK,",
               "cost and latency routing over a Redis key pool, SSE tracing."],
         metrics=[("40+", "error classes"), ("5 + 7", "apps + packages"), ("SSE", "live tracing")],
         tech=["TypeScript", "Next.js", "Redis", "Prisma", "PostgreSQL"]),
    dict(id="fraud", status="TABLEAU", idx="06", cat="DATA ANALYTICS",
         title="Fraud Detection", subtitle="Analytics on 1M card transactions",
         desc=["ETL and EDA across 50,000 accounts (2022–24), surfacing card-",
               "not-present, night-time and missing-2FA risk drivers."],
         metrics=[("1M", "transactions"), ("$12.52M", "fraud isolated"), ("1.71%", "of total volume")],
         tech=["Python", "Pandas", "Statistics", "Tableau"]),
    dict(id="rhomis", status="TABLEAU", idx="07", cat="DATA SCIENCE · TEAM",
         title="RHoMIS Analytics", subtitle="Food security across 35 countries",
         desc=["Team capstone: ETL from 1,599 variables to 46 indicators,",
               "chi-square, logistic regression and k-means profiling."],
         metrics=[("54,873", "households"), ("35", "countries"), ("7", "KPIs on Tableau")],
         tech=["Python", "scikit-learn", "K-Means", "Tableau"]),
]


LAB = [
    dict(id="auraroast", status="LIVE", idx="08", cat="COMMERCE + AI",
         title="AuraRoast", subtitle="Specialty-coffee commerce platform",
         desc=["Idempotent orders, atomic table booking, a live delivery map,",
               "UPI payments and an AI barista that fills your cart."],
         metrics=[], tech=["Next.js", "Drizzle", "PostgreSQL", "Three.js", "Groq"]),
    dict(id="axiom", status="LIVE", idx="09", cat="MULTI-MODEL AI",
         title="Axiom AI", subtitle="Multi-model AI workspace",
         desc=["Routes every task to the right engine: Groq for sub-second",
               "answers, Cerebras for deep reasoning, in one interface."],
         metrics=[], tech=["React", "Node.js", "Groq", "Cerebras"]),
    dict(id="cartify", status="LIVE", idx="10", cat="AI E-COMMERCE",
         title="Cartify AI", subtitle="AI-powered e-commerce platform",
         desc=["A conversational shopping assistant, personalised",
               "recommendations and intelligent search filtering."],
         metrics=[], tech=["MongoDB", "Express", "React", "Node.js"]),
    dict(id="traffic", status="LIVE", idx="11", cat="DEEP LEARNING",
         title="Traffic Flow", subtitle="Freeway speed forecasting on METR-LA",
         desc=["207 sensors, a leak-free pipeline, 6 forecasting baselines",
               "and experiments on what per-sensor models miss."],
         metrics=[], tech=["Python", "Deep Learning", "Streamlit"]),
]


# =====================================================================
# RECOGNITION
# =====================================================================
def achievements():
    W, H = 1000, 252
    items = [
        ("Top 20", "ALL-INDIA · 2026", "Cars24 Car-a-thon", "PIT-24: a 24-second car-cleaning line, simulated in 3D"),
        ("2025", "EMERGING TALENT", "Naukri Young Turks", "Recognised in a nationwide contest for students"),
        ("VP", "VICE PRESIDENT", "Finance Club", "FinSetu India–US collab · Zerodha-partnered quiz"),
        ("Ops", "OPERATIONS HEAD", "Esports Club", "Logistics and scheduling for campus tournaments"),
    ]
    tw, th, gap = 492, 120, 12
    tiles = []
    for i, (big, kicker, title, desc) in enumerate(items):
        x = 0 if i % 2 == 0 else tw + 16
        y = 0 if i < 2 else th + gap
        tiles.append(f'''<g >
  <rect x="{x + .5}" y="{y + .5}" width="{tw - 1}" height="{th - 1}" rx="14" fill="{SURFACE}" stroke="{LINE}"/>
  <text class="big" x="{x + 28}" y="{y + 72}">{esc(big)}</text>
  <line x1="{x + 140}" y1="{y + 28}" x2="{x + 140}" y2="{y + th - 28}" stroke="{LINE_SOFT}"/>
  <text class="k" x="{x + 162}" y="{y + 40}">{esc(kicker)}</text>
  <text class="tt" x="{x + 162}" y="{y + 66}">{esc(title)}</text>
  <text class="dd" x="{x + 162}" y="{y + 90}">{esc(desc)}</text>
</g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Recognition and leadership: Top 20 all-India at Cars24 Car-a-thon 2026; Naukri Young Turks 2025 Emerging Talent; Vice President, Finance Club; Operations Head, Esports Club">
<title>Recognition and leadership</title>
<style><![CDATA[
  {base_css()}
  .big {{ font: italic 400 40px {SERIF}; fill: {ACCENT}; }}
  .k {{ font: 500 10.5px {MONO}; letter-spacing: 1.6px; fill: {DIM}; }}
  .tt {{ font: 600 19px {SANS}; letter-spacing: -.3px; fill: {INK}; }}
  .dd {{ font: 400 13px {SANS}; fill: {MUTED}; }}
]]></style>
{''.join(tiles)}
</svg>'''
    write("achievements.svg", svg)


# =====================================================================
# FOOTER
# =====================================================================
def footer():
    W, H = 1000, 96
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Manas Saxena">
<title>Manas Saxena</title>
<style><![CDATA[
  {base_css()}
  .q {{ font: italic 400 22px {SERIF}; fill: {SOFT}; }}
  .meta {{ font: 500 11px {MONO}; letter-spacing: 1.6px; fill: {DIM}; }}
  @keyframes grow {{ from {{transform:scaleX(0)}} to {{transform:scaleX(1)}} }}
]]></style>
<line class="ln" x1="0" y1="12" x2="{W}" y2="12" stroke="{LINE}"/>
<circle cx="{W / 2}" cy="12" r="3.5" fill="{ACCENT}"/>
<text class="q" x="{W / 2}" y="54" text-anchor="middle">Make it work, make it right, make it fast — then write the test that proves it.</text>
<text class="meta" x="{W / 2}" y="84" text-anchor="middle">MANAS SAXENA <tspan fill="{FAINT}">·</tspan> FULL-STACK &amp; AI ENGINEER <tspan fill="{FAINT}">·</tspan> INDIA</text>
</svg>'''
    write("footer.svg", svg)


if __name__ == "__main__":
    header()
    about()
    stack()
    for slug, idx, label, note in [
        ("about", "01", "About", "WHO I AM"),
        ("stack", "02", "Stack", "TOOLS I SHIP WITH"),
        ("projects", "03", "Selected work", "2024 — 2026"),
        ("lab", "04", "More projects", "FROM THE LAB"),
        ("achievements", "05", "Recognition", "WINS AND ROLES"),
        ("stats", "06", "GitHub activity", "AT A GLANCE"),
        ("connect", "07", "Contact", "LET'S TALK"),
    ]:
        section(slug, idx, label, note)
    for c in CARDS + LAB:
        card(c)
    achievements()
    footer()
