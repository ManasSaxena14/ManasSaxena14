#!/usr/bin/env python3
"""Generates the animated neon SVGs used by the profile README.

Run:  python3 scripts/build_assets.py      (writes into ./assets)
Edit the DATA section below to change text, then re-run.
"""
import os
import random
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

# ---------- palette ----------
BG = "#05030d"
PANEL = "#0a0a18"
EDGE = "#1d1d3a"
CYAN = "#00f0ff"
MAGENTA = "#ff2bd6"
YELLOW = "#ffe66d"
GREEN = "#39ff14"
PURPLE = "#9d4dff"
TEXT = "#e6f1ff"
MUTED = "#8a96b8"

SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"


def esc(s):
    return escape(s, {'"': "&quot;"})


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name)


def glow_filter(fid, std=3):
    return (f'<filter id="{fid}" x="-30%" y="-30%" width="160%" height="160%">'
            f'<feGaussianBlur stdDeviation="{std}" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


# =====================================================================
# HEADER
# =====================================================================
def header():
    W, H, HZ = 1000, 320, 222
    rnd = random.Random(14)

    # skyline
    pts, wins, x = [f"0,{HZ}"], [], 0
    while x < W:
        w = rnd.randint(22, 58)
        dist = abs((x + w / 2) - W / 2)
        h = rnd.randint(8, 34) if dist < 120 else rnd.randint(20, 66)
        top = HZ - h
        pts += [f"{x},{top}", f"{x + w},{top}"]
        if rnd.random() < 0.35 and h > 40:  # antenna
            ax = x + w // 2
            pts[-1:-1] = [f"{ax - 1},{top}", f"{ax - 1},{top - 14}", f"{ax + 1},{top - 14}", f"{ax + 1},{top}"]
        for wy in range(top + 6, HZ - 4, 9):
            for wx in range(x + 4, x + w - 4, 8):
                if rnd.random() < 0.22:
                    c = rnd.choice([YELLOW, CYAN, MAGENTA, YELLOW])
                    d = rnd.uniform(0, 6)
                    wins.append(f'<rect class="win" x="{wx}" y="{wy}" width="3" height="4" fill="{c}" style="animation-delay:-{d:.2f}s"/>')
        x += w + rnd.randint(0, 3)
    pts.append(f"{W},{HZ}")
    skyline = " ".join(pts)

    stars = "".join(
        f'<circle class="star" cx="{rnd.randint(10, W - 10)}" cy="{rnd.randint(8, 150)}" r="{rnd.choice([0.6, 0.9, 1.2])}" '
        f'fill="#fff" style="animation-delay:-{rnd.uniform(0, 4):.2f}s"/>' for _ in range(70))

    vlines = "".join(
        f'<line x1="{500 + k * 16}" y1="{HZ}" x2="{500 + k * 110}" y2="{H}" />' for k in range(-14, 15))
    hlines = "".join(
        f'<line class="hl" x1="0" y1="{HZ}" x2="{W}" y2="{HZ}" style="animation-delay:-{i * 0.5:.2f}s"/>' for i in range(7))

    particles = "".join(
        f'<circle class="pt" cx="{rnd.randint(20, W - 20)}" cy="{rnd.randint(200, 310)}" r="{rnd.choice([1, 1.4, 2])}" '
        f'fill="{rnd.choice([CYAN, MAGENTA, YELLOW])}" style="animation-delay:-{rnd.uniform(0, 7):.2f}s;animation-duration:{rnd.uniform(5, 9):.2f}s"/>'
        for _ in range(26))

    sun_stripes = "".join(
        f'<rect x="400" y="{HZ - 46 + i * 9 + i * i * 0.6:.1f}" width="200" height="{1.5 + i * 0.9:.1f}" fill="#000"/>' for i in range(6))

    name = "MANAS SAXENA"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Manas Saxena — Full-Stack and AI Engineer">
<title>Manas Saxena — Full-Stack + AI Engineer</title>
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#030210"/><stop offset=".6" stop-color="#140530"/><stop offset="1" stop-color="#2a0640"/>
  </linearGradient>
  <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1a0233"/><stop offset="1" stop-color="#05010c"/>
  </linearGradient>
  <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{YELLOW}"/><stop offset=".55" stop-color="#ff6ec7"/><stop offset="1" stop-color="{MAGENTA}"/>
  </linearGradient>
  <linearGradient id="nameFill" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#9ff8ff"/>
  </linearGradient>
  <linearGradient id="frame" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{MAGENTA}"/>
  </linearGradient>
  <linearGradient id="scanband" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".10"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".35"/></pattern>
  <mask id="sunMask"><rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>{sun_stripes}</mask>
  <clipPath id="frameClip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18"/></clipPath>
  <clipPath id="groundClip"><rect x="0" y="{HZ}" width="{W}" height="{H - HZ}"/></clipPath>
  <clipPath id="band1"><rect x="0" y="66" width="{W}" height="18"/></clipPath>
  <clipPath id="band2"><rect x="0" y="92" width="{W}" height="14"/></clipPath>
  {glow_filter("g2", 2)}{glow_filter("g6", 6)}{glow_filter("g12", 12)}
</defs>
<style><![CDATA[
  .hud {{ font: 600 11px {MONO}; fill: {CYAN}; letter-spacing: 2px; opacity: .75; }}
  .name {{ font: 900 66px {SANS}; letter-spacing: 10px; }}
  .role {{ font: 700 17px {MONO}; letter-spacing: 7px; fill: {CYAN}; }}
  .win {{ animation: tw 6s steps(1) infinite; }}
  .star {{ animation: st 4s ease-in-out infinite; }}
  .hl {{ animation: hl 3.5s cubic-bezier(.55,0,1,.45) infinite; }}
  .pt {{ animation: pt 7s linear infinite; }}
  .sun {{ animation: sun 5s ease-in-out infinite; transform-origin: 500px {HZ}px; }}
  .flick {{ animation: flick 5s linear infinite; }}
  .gA {{ animation: gA 4.5s steps(1) infinite; }}
  .gB {{ animation: gB 4.5s steps(1) infinite; }}
  .blink {{ animation: blink 1.2s steps(1) infinite; }}
  .scanband {{ animation: sb 6s linear infinite; }}
  .frame {{ stroke-dasharray: 260 2300; animation: fr 7s linear infinite; }}
  .intro {{ animation: intro 1.4s cubic-bezier(.2,.8,.2,1) both; }}
  @keyframes tw {{ 0%,100% {{opacity:.9}} 37% {{opacity:.15}} 52% {{opacity:.9}} 81% {{opacity:.4}} }}
  @keyframes st {{ 0%,100% {{opacity:.15}} 50% {{opacity:1}} }}
  @keyframes hl {{ from {{transform:translateY(0);opacity:.1}} to {{transform:translateY({H - HZ}px);opacity:1}} }}
  @keyframes pt {{ from {{transform:translateY(0);opacity:0}} 15% {{opacity:.9}} to {{transform:translateY(-200px);opacity:0}} }}
  @keyframes sun {{ 0%,100% {{opacity:.9}} 50% {{opacity:1}} }}
  @keyframes flick {{ 0%,19%,21%,62%,64%,66%,100% {{opacity:1}} 20%,63%,65% {{opacity:.25}} }}
  @keyframes gA {{ 0%,86%,100% {{opacity:0;transform:translate(0,0)}} 87% {{opacity:.95;transform:translate(-7px,0)}} 89% {{opacity:.95;transform:translate(5px,-1px)}} 91% {{opacity:.9;transform:translate(-3px,1px)}} 93% {{opacity:0}} }}
  @keyframes gB {{ 0%,87%,100% {{opacity:0;transform:translate(0,0)}} 88% {{opacity:.95;transform:translate(6px,0)}} 90% {{opacity:.9;transform:translate(-5px,1px)}} 92% {{opacity:.9;transform:translate(3px,0)}} 94% {{opacity:0}} }}
  @keyframes blink {{ 0%,100% {{opacity:1}} 50% {{opacity:.15}} }}
  @keyframes sb {{ from {{transform:translateY(-60px)}} to {{transform:translateY({H + 60}px)}} }}
  @keyframes fr {{ from {{stroke-dashoffset:0}} to {{stroke-dashoffset:-2560}} }}
  @keyframes intro {{ from {{opacity:0;transform:translateY(14px);filter:blur(6px)}} to {{opacity:1;transform:none;filter:none}} }}
]]></style>
<g clip-path="url(#frameClip)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  {stars}
  <circle cx="500" cy="{HZ}" r="96" fill="{MAGENTA}" opacity=".18" filter="url(#g12)"/>
  <g class="sun" mask="url(#sunMask)"><circle cx="500" cy="{HZ}" r="70" fill="url(#sun)"/></g>
  <polygon points="{skyline}" fill="#07020f"/>
  <polyline points="{skyline}" fill="none" stroke="{MAGENTA}" stroke-width="1.2" opacity=".8" filter="url(#g2)"/>
  {''.join(wins)}
  <rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#ground)"/>
  <g clip-path="url(#groundClip)" stroke="{MAGENTA}" stroke-width="1" opacity=".55">{vlines}</g>
  <g clip-path="url(#groundClip)" stroke="{CYAN}" stroke-width="1.2" opacity=".7">{hlines}</g>
  <line x1="0" y1="{HZ}" x2="{W}" y2="{HZ}" stroke="{CYAN}" stroke-width="2" filter="url(#g6)"/>
  {particles}

  <g class="intro">
    <text class="name" x="500" y="104" text-anchor="middle" fill="none" stroke="{CYAN}" stroke-width="2" opacity=".55" filter="url(#g12)">{name}</text>
    <text class="name" x="500" y="104" text-anchor="middle" fill="url(#nameFill)" filter="url(#g2)">{name}</text>
    <g clip-path="url(#band1)"><text class="name gA" x="500" y="104" text-anchor="middle" fill="{CYAN}">{name}</text></g>
    <g clip-path="url(#band2)"><text class="name gB" x="500" y="104" text-anchor="middle" fill="{MAGENTA}">{name}</text></g>
    <text class="role flick" x="500" y="142" text-anchor="middle" filter="url(#g2)">FULL-STACK <tspan fill="{MAGENTA}">+</tspan> AI ENGINEER</text>
  </g>

  <text class="hud" x="28" y="32">// SYS.BOOT :: MANAS.EXE</text>
  <text class="hud" x="972" y="32" text-anchor="end"><tspan class="blink" fill="{GREEN}">●</tspan> ONLINE</text>
  <text class="hud" x="28" y="300">NODE://INDIA · NST × RISHIHOOD</text>
  <text class="hud" x="972" y="300" text-anchor="end">BUILD 2026.11 <tspan class="blink">▮</tspan></text>
  <g fill="none" stroke="{CYAN}" stroke-width="2" opacity=".8">
    <path d="M14 40 V14 H40"/><path d="M{W - 40} 14 H{W - 14} V40"/>
    <path d="M14 {H - 40} V{H - 14} H40"/><path d="M{W - 40} {H - 14} H{W - 14} V{H - 40}"/>
  </g>
  <rect width="{W}" height="{H}" fill="url(#scan)"/>
  <rect class="scanband" y="0" width="{W}" height="60" fill="url(#scanband)"/>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="{EDGE}" stroke-width="2"/>
<rect class="frame" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="url(#frame)" stroke-width="2.5" filter="url(#g2)"/>
</svg>'''
    write("header.svg", svg)


# =====================================================================
# TERMINAL (about me)
# =====================================================================
def terminal():
    W = 1000
    FS, LH, X0, CW = 14, 27, 34, 8.6
    P = [("manas", GREEN), ("@", MUTED), ("nst", CYAN), (":", MUTED), ("~", PURPLE), ("$ ", MUTED)]

    def kv(k, v):
        return [(f"{k:<13}", MAGENTA), (": ", MUTED), (v, TEXT)]

    lines = [
        (P + [("whoami", YELLOW)], "cmd"),
        ([("Manas Vivek Saxena — a Full-Stack + AI Engineer who ships production-grade systems.", TEXT)], "out"),
        ([("", TEXT)], "out"),
        (P + [("cat profile.yaml", YELLOW)], "cmd"),
        (kv("education", "B.Tech CS & AI · Newton School of Technology × Rishihood University · 2024–28"), "out"),
        (kv("i_build", "LLM gateways · agentic AI pipelines · race-safe backends · data stories"), "out"),
        (kv("core_stack", "TypeScript · Next.js · NestJS · FastAPI · PostgreSQL · Redis · LangGraph"), "out"),
        (kv("obsessed_with", "concurrency, correctness, test coverage & p95 latency"), "out"),
        (kv("off_keyboard", "VP, Finance Club (FinSetu India–US) · Ops Head, Esports Club"), "out"),
        (kv("open_to", "internships · collaborations · hard engineering problems"), "out"),
        ([("", TEXT)], "out"),
        (P, "end"),
    ]
    H = 58 + len(lines) * LH + 22
    T = 18.0  # loop period (s)

    # timings
    t, timings = 0.6, []
    for segs, kind in lines:
        n = sum(len(s) for s, _ in segs)
        if kind == "cmd":
            pn = sum(len(s) for s, _ in P)
            dur = max(0.4, (n - pn) / 14)
        elif kind == "end":
            dur = 0.05
        else:
            dur = max(0.05, n / 70)
        timings.append((t, dur, n))
        t += dur + (0.35 if kind == "cmd" else 0.08)

    css, body = [], []
    for i, ((segs, kind), (start, dur, n)) in enumerate(zip(lines, timings)):
        y = 58 + 14 + i * LH
        spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in segs)
        body.append(f'<clipPath id="cl{i}"><rect class="c{i}" x="{X0 - 2 - W}" y="{y - 18}" width="{W}" height="{LH}"/></clipPath>')
        body.append(f'<g clip-path="url(#cl{i})"><text x="{X0}" y="{y}" xml:space="preserve" class="t">{spans}</text>')
        if kind == "end":
            cx = X0 + n * CW
            body.append(f'<rect class="cur" x="{cx:.1f}" y="{y - 13}" width="9" height="17" fill="{CYAN}"/>')
        body.append('</g>')
        a, b = start / T * 100, (start + dur) / T * 100
        L = n * CW * 1.12 + 14
        steps = max(1, n if kind != "cmd" else n - sum(len(s) for s, _ in P))
        pre = sum(len(s) for s, _ in P) * CW * 1.12 if kind == "cmd" else 0
        css.append(
            f"@keyframes r{i} {{ 0% {{transform:translateX(0)}} {max(a - 0.01, 0):.2f}% {{transform:translateX(0)}} {a:.2f}%{{transform:translateX({pre:.1f}px);animation-timing-function:steps({steps},end)}} "
            f"{b:.2f}% {{transform:translateX({L:.1f}px)}} 100% {{transform:translateX({L:.1f}px)}} }}"
            f".c{i} {{ animation: r{i} {T}s linear infinite; }}")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="About Manas: terminal profile">
<title>whoami — Manas Saxena</title>
<defs>
  <clipPath id="clip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>
  <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="#11112a"/><stop offset="1" stop-color="#1a0a2a"/></linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>
  <radialGradient id="glowC" cx=".9" cy="0" r=".7"><stop offset="0" stop-color="{MAGENTA}" stop-opacity=".16"/><stop offset="1" stop-color="{MAGENTA}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glowL" cx="0" cy="1" r=".7"><stop offset="0" stop-color="{CYAN}" stop-opacity=".10"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".25"/></pattern>
  {glow_filter("g2", 2)}
</defs>
<style><![CDATA[
  .t {{ font: 500 {FS}px {MONO}; }}
  .bar {{ font: 600 12px {MONO}; fill: {MUTED}; letter-spacing: 1px; }}
  .cur {{ animation: blink 1s steps(1) infinite; }}
  .all {{ animation: fade {T}s linear infinite; }}
  .frame {{ stroke-dasharray: 200 2400; animation: fr 8s linear infinite; }}
  @keyframes blink {{ 0%,100% {{opacity:1}} 50% {{opacity:0}} }}
  @keyframes fade {{ 0% {{opacity:0}} 2% {{opacity:1}} 95% {{opacity:1}} 100% {{opacity:0}} }}
  @keyframes fr {{ from {{stroke-dashoffset:0}} to {{stroke-dashoffset:-2600}} }}
  {"".join(css)}
]]></style>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="{PANEL}"/>
  <rect width="{W}" height="{H}" fill="url(#glowC)"/><rect width="{W}" height="{H}" fill="url(#glowL)"/>
  <rect width="{W}" height="40" fill="url(#bar)"/>
  <line x1="0" y1="40" x2="{W}" y2="40" stroke="{EDGE}"/>
  <circle cx="24" cy="20" r="6" fill="#ff5f57"/><circle cx="44" cy="20" r="6" fill="#febc2e"/><circle cx="64" cy="20" r="6" fill="#28c840"/>
  <text class="bar" x="{W / 2}" y="24" text-anchor="middle">manas@nst: ~/profile — zsh — 120×{len(lines)}</text>
  <text class="bar" x="{W - 22}" y="24" text-anchor="end" fill="{CYAN}">LIVE</text>
  <g class="all">{"".join(body)}</g>
  <rect width="{W}" height="{H}" fill="url(#scan)"/>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{EDGE}" stroke-width="2"/>
<rect class="frame" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="url(#edge)" stroke-width="2" filter="url(#g2)"/>
</svg>'''
    write("terminal.svg", svg)


# =====================================================================
# SECTION TITLES
# =====================================================================
def section(slug, idx, label, accent):
    W, H = 1000, 58
    tl = (len(label) + 3) * 18.6 - 3  # forced text width, so cursor/line never collide with the label
    tw = tl + 52
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}">
<title>{esc(label)}</title>
<defs>
  <linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>
  <linearGradient id="comet" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
  {glow_filter("g", 3)}
</defs>
<style><![CDATA[
  .lbl {{ font: 800 26px {MONO}; letter-spacing: 3px; fill: {TEXT}; }}
  .idx {{ font: 700 12px {MONO}; letter-spacing: 2px; fill: {accent}; }}
  .cur {{ animation: b 1s steps(1) infinite; }}
  .comet {{ animation: c 3.2s cubic-bezier(.6,0,.4,1) infinite; }}
  .in {{ animation: in .9s cubic-bezier(.2,.8,.2,1) both; }}
  .gl {{ animation: gl 5s steps(1) infinite; }}
  @keyframes b {{ 0%,100% {{opacity:1}} 50% {{opacity:0}} }}
  @keyframes c {{ from {{transform:translateX({tw:.0f}px);opacity:0}} 10% {{opacity:1}} 90% {{opacity:1}} to {{transform:translateX({W - 60}px);opacity:0}} }}
  @keyframes in {{ from {{opacity:0;transform:translateX(-18px)}} to {{opacity:1;transform:none}} }}
  @keyframes gl {{ 0%,90%,100% {{transform:none;opacity:0}} 91% {{transform:translate(-3px,0);opacity:.85}} 93% {{transform:translate(3px,1px);opacity:.85}} 95% {{opacity:0}} }}
]]></style>
<g class="in">
  <text class="idx" x="2" y="14">{idx}</text>
  <text class="lbl" x="0" y="44" filter="url(#g)" textLength="{tl:.0f}" lengthAdjust="spacingAndGlyphs"><tspan fill="{accent}">&gt;_ </tspan>{esc(label)}</text>
  <text class="lbl gl" x="0" y="44" fill="{MAGENTA if accent != MAGENTA else CYAN}" opacity="0" textLength="{tl:.0f}" lengthAdjust="spacingAndGlyphs"><tspan>&gt;_ </tspan>{esc(label)}</text>
  <rect class="cur" x="{tl + 10:.0f}" y="24" width="12" height="24" fill="{accent}"/>
</g>
<line x1="{tw:.0f}" y1="36" x2="{W}" y2="36" stroke="url(#ln)" stroke-width="2" opacity=".7"/>
<g class="comet"><rect x="-60" y="34.5" width="60" height="3" rx="1.5" fill="url(#comet)" filter="url(#g)"/></g>
</svg>'''
    write(f"section_{slug}.svg", svg)


# =====================================================================
# PROJECT CARDS
# =====================================================================
def pill_w(t):
    return len(t) * 7.3 + 20


def card(c):
    W = c.get("W", 500)
    py = 244 if c["metrics"] else 166
    H = py + 48
    a, a2 = c["accent"], c["accent2"]
    cid = c["id"]
    metrics = c["metrics"]
    gap = 10
    mw = (W - 48 - gap * (len(metrics) - 1)) / max(len(metrics), 1)

    mboxes = []
    for i, (num, lbl) in enumerate(metrics):
        x = 24 + i * (mw + gap)
        mboxes.append(f'''<g class="m" style="animation-delay:{0.25 + i * 0.15:.2f}s">
    <rect x="{x:.1f}" y="166" width="{mw:.1f}" height="62" rx="8" fill="#0f0f24" stroke="{EDGE}"/>
    <rect class="mbar" x="{x:.1f}" y="166" width="{mw:.1f}" height="2" rx="1" fill="{a}" style="animation-delay:{0.4 + i * 0.15:.2f}s"/>
    <text class="mn" x="{x + 14:.1f}" y="198" fill="{a if i % 2 == 0 else a2}">{esc(num)}</text>
    <text class="ml" x="{x + 14:.1f}" y="217">{esc(lbl)}</text></g>''')

    pills, px = [], 24
    for t in c["tech"]:
        w = pill_w(t)
        pills.append(f'<rect x="{px:.1f}" y="{py}" width="{w:.1f}" height="24" rx="12" fill="none" stroke="{a}" stroke-opacity=".45"/>'
                     f'<text class="pl" x="{px + w / 2:.1f}" y="{py + 16}" text-anchor="middle">{esc(t)}</text>')
        px += w + 8

    desc = "".join(f'<text class="d" x="24" y="{130 + i * 18}">{esc(l)}</text>' for i, l in enumerate(c["desc"]))
    chip = c["chip"]
    chip_w = len(chip) * 9 + 30
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(c['title'])} — {esc(c['subtitle'])}">
<title>{esc(c['title'])} — {esc(c['subtitle'])}</title>
<defs>
  <clipPath id="clip-{cid}"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>
  <radialGradient id="rg-{cid}" cx="1" cy="0" r=".9"><stop offset="0" stop-color="{a}" stop-opacity=".22"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>
  <radialGradient id="rg2-{cid}" cx="0" cy="1" r=".8"><stop offset="0" stop-color="{a2}" stop-opacity=".12"/><stop offset="1" stop-color="{a2}" stop-opacity="0"/></radialGradient>
  <linearGradient id="sb-{cid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset=".5" stop-color="{a}" stop-opacity=".09"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>
  <pattern id="grid-{cid}" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="#ffffff" stroke-opacity=".035"/></pattern>
  {glow_filter("g-" + cid, 2.5)}
</defs>
<style><![CDATA[
  .tag {{ font: 700 11px {MONO}; letter-spacing: 2px; fill: {a}; }}
  .ti {{ font: 900 30px {SANS}; letter-spacing: 2px; fill: {TEXT}; }}
  .st {{ font: 600 14px {SANS}; fill: #c9d1ff; }}
  .d {{ font: 400 13px {SANS}; fill: {MUTED}; }}
  .mn {{ font: 800 22px {MONO}; }}
  .ml {{ font: 500 10.5px {MONO}; fill: {MUTED}; letter-spacing: .5px; }}
  .pl {{ font: 600 11px {MONO}; fill: #c9d1ff; }}
  .chip {{ font: 700 10.5px {MONO}; letter-spacing: 2px; fill: {GREEN}; }}
  .sweep1 {{ stroke-dasharray: 110 890; animation: sw 6s linear infinite; }}
  .sweep2 {{ stroke-dasharray: 60 940; animation: sw 6s linear infinite; animation-delay: -3s; }}
  .scan {{ animation: scan 4.5s linear infinite; }}
  .m {{ animation: up .7s cubic-bezier(.2,.8,.2,1) both; }}
  .mbar {{ transform-box: fill-box; transform-origin: left; animation: grow 1s cubic-bezier(.2,.8,.2,1) both; }}
  .dot {{ animation: blink 1.4s ease-in-out infinite; }}
  .ring {{ transform-box: fill-box; transform-origin: center; animation: ring 1.8s ease-out infinite; }}
  .gl {{ animation: gl 6s steps(1) infinite; }}
  .br {{ animation: br 3s ease-in-out infinite; }}
  @keyframes sw {{ from {{stroke-dashoffset:0}} to {{stroke-dashoffset:-1000}} }}
  @keyframes scan {{ from {{transform:translateY(-70px)}} to {{transform:translateY({H + 10}px)}} }}
  @keyframes up {{ from {{opacity:0;transform:translateY(10px)}} to {{opacity:1;transform:none}} }}
  @keyframes grow {{ from {{transform:scaleX(0)}} to {{transform:scaleX(1)}} }}
  @keyframes blink {{ 0%,100% {{opacity:1}} 50% {{opacity:.3}} }}
  @keyframes ring {{ from {{transform:scale(1);opacity:.8}} to {{transform:scale(3);opacity:0}} }}
  @keyframes gl {{ 0%,92%,100% {{opacity:0;transform:none}} 93% {{opacity:.8;transform:translate(-4px,0)}} 95% {{opacity:.8;transform:translate(3px,1px)}} 97% {{opacity:0}} }}
  @keyframes br {{ 0%,100% {{opacity:.9}} 50% {{opacity:.35}} }}
]]></style>
<g clip-path="url(#clip-{cid})">
  <rect width="{W}" height="{H}" fill="{PANEL}"/>
  <rect width="{W}" height="{H}" fill="url(#grid-{cid})"/>
  <rect width="{W}" height="{H}" fill="url(#rg-{cid})"/><rect width="{W}" height="{H}" fill="url(#rg2-{cid})"/>
  <rect class="scan" width="{W}" height="70" fill="url(#sb-{cid})"/>
  <text class="tag" x="24" y="36">{esc(c['tag'])}</text>
  <g>
    <rect x="{W - 24 - chip_w:.1f}" y="21" width="{chip_w:.1f}" height="22" rx="11" fill="#0d1f12" stroke="{GREEN}" stroke-opacity=".5"/>
    <circle class="ring" cx="{W - 24 - chip_w + 13:.1f}" cy="32" r="3.5" fill="none" stroke="{GREEN}"/>
    <circle class="dot" cx="{W - 24 - chip_w + 13:.1f}" cy="32" r="3.5" fill="{GREEN}"/>
    <text class="chip" x="{W - 24 - chip_w + 23:.1f}" y="36">{esc(chip)}</text>
  </g>
  <text class="ti" x="24" y="80" filter="url(#g-{cid})">{esc(c['title'])}</text>
  <text class="ti gl" x="24" y="80" style="fill:{a2}">{esc(c['title'])}</text>
  <text class="st" x="24" y="104">{esc(c['subtitle'])}</text>
  {desc}
  {''.join(mboxes)}
  {''.join(pills)}
  <g class="br" fill="none" stroke="{a}" stroke-width="2">
    <path d="M8 26 V8 H26"/><path d="M{W - 26} {H - 8} H{W - 8} V{H - 26}"/>
  </g>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{EDGE}" stroke-width="1.5"/>
<rect class="sweep1" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{a}" stroke-width="2.5" pathLength="1000" filter="url(#g-{cid})"/>
<rect class="sweep2" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{a2}" stroke-width="2" pathLength="1000" filter="url(#g-{cid})"/>
</svg>'''
    write(f"card_{cid}.svg", svg)


CARDS = [
    dict(id="hireflow", W=1000, accent=MAGENTA, accent2=CYAN, chip="LIVE", tag="01 // SPOTLIGHT · HIRING PLATFORM + ATS",
         title="HIREFLOW", subtitle="Two-sided hiring platform & applicant tracking system",
         desc=["Job seekers track every application; companies post jobs, run their hiring pipeline and book interviews with 4-role RBAC.",
               "Double-booking is impossible via Postgres exclusion constraints (verified at 20 concurrent bookings); resumes scored by TF-IDF."],
         metrics=[("441", "tests in CI"), ("97%", "API coverage"),
                  ("<25ms", "p95 @ 50 concurrent users"), ("7", "pg-boss job queues")],
         tech=["Next.js", "NestJS", "PostgreSQL", "pg-boss", "TF-IDF", "RBAC", "Vercel", "Render"]),
    dict(id="finsight", accent=GREEN, accent2=CYAN, chip="LIVE", tag="02 // AI FINTECH",
         title="FINSIGHT AI", subtitle="Personal-finance forecasting & advisory",
         desc=["Time-series spend forecasts, overspend risk, anomaly detection and",
               "Monte Carlo goal planning + tool-calling LLM advisor with guardrails."],
         metrics=[("RAG", "grounded advisor"), ("PII", "guardrails"), ("Docker", "+ CI/CD")],
         tech=["FastAPI", "React", "MongoDB", "scikit-learn", "Docker"]),
    dict(id="bidverse", accent=YELLOW, accent2=MAGENTA, chip="LIVE", tag="03 // REAL-TIME MARKETPLACE",
         title="BIDVERSE", subtitle="MERN auction marketplace",
         desc=["Race-safe bidding: simultaneous equal bids resolve to one winner",
               "and one HTTP 409. Idempotent bids, auto-settled 10% commission."],
         metrics=[("30+", "REST APIs"), ("16", "pages shipped"), ("6", "Mongo pipelines")],
         tech=["React", "Node.js", "Express", "MongoDB", "Groq AI"]),
    dict(id="churnly", accent=PURPLE, accent2=CYAN, chip="LIVE", tag="04 // AGENTIC AI",
         title="CHURNLY", subtitle="Explains why customers churn",
         desc=["21-node LangGraph pipeline: survival analysis, BH-corrected stats,",
               "adversarial LLM review, RAG + Monte Carlo → cited retention playbook."],
         metrics=[("21", "LangGraph nodes"), ("CoxPH", "+ Kaplan-Meier"), ("CI", "tested pipeline")],
         tech=["LangGraph", "FastAPI", "Next.js", "DuckDB", "RAG"]),
    dict(id="orbyt", accent=CYAN, accent2=MAGENTA, chip="LIVE", tag="05 // LLM INFRASTRUCTURE",
         title="ORBYT", subtitle="Self-hosted OpenAI-compatible LLM gateway",
         desc=["Drop-in /v1/chat/completions with fallback chains, BYOK,",
               "cost + latency routing over a Redis key pool and SSE tracing."],
         metrics=[("40+", "error classes"), ("5 + 7", "apps + packages"), ("SSE", "live tracing")],
         tech=["TypeScript", "Next.js", "Redis", "Prisma", "PostgreSQL"]),
    dict(id="fraud", accent=MAGENTA, accent2=YELLOW, chip="TABLEAU", tag="06 // DATA ANALYTICS",
         title="FRAUD DETECTION", subtitle="Analytics on 1M card transactions",
         desc=["ETL + EDA across 50,000 accounts (2022–24) surfacing card-not-present,",
               "night-time and missing-2FA risk drivers in a Tableau fraud monitor."],
         metrics=[("1M", "transactions"), ("$12.52M", "fraud isolated"), ("1.71%", "of total volume")],
         tech=["Python", "Pandas", "Statistics", "Tableau"]),
    dict(id="rhomis", accent=CYAN, accent2=GREEN, chip="TABLEAU", tag="07 // DATA SCIENCE · TEAM",
         title="RHoMIS ANALYTICS", subtitle="Food security across 35 countries",
         desc=["Team capstone: ETL from 1,599 variables to 46 indicators, chi-square,",
               "logistic regression and k-means vulnerability profiling."],
         metrics=[("54,873", "households"), ("35", "countries"), ("7", "KPIs on Tableau")],
         tech=["Python", "scikit-learn", "K-Means", "Tableau"]),
]


LAB = [
    dict(id="auraroast", accent=YELLOW, accent2=MAGENTA, chip="LIVE", tag="08 // COMMERCE + AI",
         title="AURAROAST", subtitle="Specialty-coffee commerce platform",
         desc=["Idempotent orders, atomic table booking, live delivery map,",
               "UPI payments and a tool-calling AI barista that fills your cart."],
         metrics=[], tech=["Next.js", "Drizzle", "PostgreSQL", "Three.js", "Groq"]),
    dict(id="axiom", accent=CYAN, accent2=PURPLE, chip="LIVE", tag="09 // MULTI-MODEL AI",
         title="AXIOM AI", subtitle="Multi-model AI workspace",
         desc=["Routes every task to the right engine: Groq for sub-second",
               "answers, Cerebras for deep reasoning, in one secure interface."],
         metrics=[], tech=["React", "Node.js", "Groq", "Cerebras"]),
    dict(id="cartify", accent=MAGENTA, accent2=CYAN, chip="LIVE", tag="10 // AI E-COMMERCE",
         title="CARTIFY AI", subtitle="AI-powered e-commerce platform",
         desc=["Conversational shopping assistant, personalised",
               "recommendations and intelligent search filtering."],
         metrics=[], tech=["MongoDB", "Express", "React", "Node.js"]),
    dict(id="traffic", accent=GREEN, accent2=YELLOW, chip="LIVE", tag="11 // DEEP LEARNING",
         title="TRAFFIC FLOW", subtitle="Freeway speed forecasting on METR-LA",
         desc=["207 sensors, a leak-free pipeline, 6 forecasting baselines",
               "and experiments on what per-sensor models miss."],
         metrics=[], tech=["Python", "Deep Learning", "Streamlit"]),
]


# =====================================================================
# ACHIEVEMENTS
# =====================================================================
def achievements():
    W, H = 1000, 236
    items = [
        ("20", "TOP 20 · ALL-INDIA", "Cars24 Car-a-thon 2026", "PIT-24: a 24-second car-cleaning line, 3D-simulated", YELLOW),
        ("YT", "EMERGING TALENT", "Naukri Young Turks 2025", "Recognised in a nationwide contest for college students", CYAN),
        ("VP", "VICE PRESIDENT", "Finance Club", "FinSetu India–US collab · Zerodha-partnered quiz", MAGENTA),
        ("OPS", "OPERATIONS HEAD", "Esports Club", "Logistics & scheduling for campus tournaments", GREEN),
    ]
    tiles = []
    for i, (glyph, kicker, title, desc, col) in enumerate(items):
        cx, cy = (0 if i % 2 == 0 else 508), (0 if i < 2 else 122)
        hx, hy = cx + 54, cy + 57
        hexp = " ".join(f"{hx + 30 * x:.1f},{hy + 30 * y:.1f}" for x, y in
                        [(0, -1), (.866, -.5), (.866, .5), (0, 1), (-.866, .5), (-.866, -.5)])
        fs = 20 if len(glyph) < 3 else 16
        tiles.append(f'''<g class="tile" style="animation-delay:{i * 0.18:.2f}s">
  <rect x="{cx + 1}" y="{cy + 1}" width="490" height="112" rx="12" fill="{PANEL}" stroke="{EDGE}"/>
  <rect x="{cx + 1}" y="{cy + 1}" width="490" height="112" rx="12" fill="none" stroke="{col}" stroke-width="2" pathLength="1000" class="sw" style="animation-delay:-{i * 1.4:.1f}s"/>
  <polygon class="hex" points="{hexp}" fill="{col}" fill-opacity=".08" stroke="{col}" stroke-width="2" filter="url(#g)" style="animation-delay:-{i * 0.7:.1f}s"/>
  <text x="{hx}" y="{hy + fs * 0.36:.1f}" text-anchor="middle" style="font:900 {fs}px {MONO};fill:{col}">{esc(glyph)}</text>
  <text class="k" x="{cx + 104}" y="{cy + 36}" fill="{col}">{esc(kicker)}</text>
  <text class="tt" x="{cx + 104}" y="{cy + 64}">{esc(title)}</text>
  <text class="dd" x="{cx + 104}" y="{cy + 88}">{esc(desc)}</text>
</g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Achievements and leadership">
<title>Achievements and leadership</title>
<defs>{glow_filter("g", 3)}</defs>
<style><![CDATA[
  .k {{ font: 700 11px {MONO}; letter-spacing: 2px; }}
  .tt {{ font: 800 20px {SANS}; fill: {TEXT}; }}
  .dd {{ font: 400 13px {SANS}; fill: {MUTED}; }}
  .tile {{ animation: up .8s cubic-bezier(.2,.8,.2,1) both; }}
  .hex {{ animation: pulse 2.6s ease-in-out infinite; }}
  .sw {{ stroke-dasharray: 80 920; animation: sw 7s linear infinite; }}
  @keyframes up {{ from {{opacity:0;transform:translateY(12px)}} to {{opacity:1;transform:none}} }}
  @keyframes pulse {{ 0%,100% {{fill-opacity:.06;stroke-opacity:1}} 50% {{fill-opacity:.22;stroke-opacity:.5}} }}
  @keyframes sw {{ from {{stroke-dashoffset:0}} to {{stroke-dashoffset:-1000}} }}
]]></style>
{''.join(tiles)}
</svg>'''
    write("achievements.svg", svg)


if __name__ == "__main__":
    header()
    terminal()
    for slug, idx, label, acc in [
        ("about", "0x01", "WHOAMI", CYAN),
        ("stack", "0x02", "TECH_ARSENAL", MAGENTA),
        ("projects", "0x03", "FEATURED_BUILDS", YELLOW),
        ("lab", "0x04", "MORE_FROM_THE_LAB", PURPLE),
        ("achievements", "0x05", "WINS_AND_ROLES", GREEN),
        ("stats", "0x06", "GITHUB_TELEMETRY", CYAN),
        ("connect", "0x07", "OPEN_A_CHANNEL", MAGENTA),
    ]:
        section(slug, idx, label, acc)
    for c in CARDS + LAB:
        card(c)
    achievements()
