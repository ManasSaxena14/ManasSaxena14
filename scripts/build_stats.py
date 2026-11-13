#!/usr/bin/env python3
"""Self-hosted, neon-themed GitHub stats (no third-party stats service needed).

Runs inside the GitHub Action with GITHUB_TOKEN and writes:
  dist/stats.svg      headline numbers
  dist/languages.svg  top languages (by bytes, own non-fork repos)
  dist/activity.svg   contribution activity, last 60 days

Local run:  GITHUB_TOKEN=$(gh auth token) python3 scripts/build_stats.py ManasSaxena14 dist
"""
import json
import os
import sys
import urllib.request
from datetime import date
from xml.sax.saxutils import escape

LOGIN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REPOSITORY_OWNER", "ManasSaxena14")
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist"
os.makedirs(OUT, exist_ok=True)

PANEL, EDGE = "#0a0a18", "#1d1d3a"
CYAN, MAGENTA, YELLOW, GREEN, PURPLE = "#00f0ff", "#ff2bd6", "#ffe66d", "#39ff14", "#9d4dff"
TEXT, MUTED = "#e6f1ff", "#8a96b8"
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
SKIP_LANGS = {"Jupyter Notebook", "HTML", "CSS", "SCSS", "Shell", "Dockerfile", "Makefile", "Procfile", "Batchfile"}
LANG_COLORS = [CYAN, MAGENTA, YELLOW, PURPLE, GREEN, "#ff8a00", "#4dd2ff", "#ff6ec7"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    pullRequests { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100, privacy: PUBLIC) {
      totalCount
      nodes { stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
}"""


def gql():
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]["user"]


def glow(fid, std=2.5):
    return (f'<filter id="{fid}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{std}" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def frame(W, H, inner, extra_css="", defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><clipPath id="clip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>
<pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>
{glow("g")}{defs}</defs>
<style><![CDATA[
.h {{ font: 700 11px {MONO}; letter-spacing: 2px; fill: {CYAN}; }}
.fr {{ stroke-dasharray: 90 910; animation: fr 7s linear infinite; }}
@keyframes fr {{ from {{stroke-dashoffset:0}} to {{stroke-dashoffset:-1000}} }}
@keyframes up {{ from {{opacity:0;transform:translateY(10px)}} to {{opacity:1;transform:none}} }}
{extra_css}
]]></style>
<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="{PANEL}"/><rect width="{W}" height="{H}" fill="url(#grid)"/>{inner}</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{EDGE}" stroke-width="1.5"/>
<rect class="fr" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="url(#edge)" stroke-width="2" pathLength="1000" filter="url(#g)"/>
</svg>'''


def fmt(n):
    return f"{n / 1000:.1f}k" if n >= 10000 else f"{n:,}"


def stats_svg(u):
    cc = u["contributionsCollection"]
    active = sum(1 for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"] if d["contributionCount"] > 0)
    tiles = [
        ("CONTRIBUTIONS", cc["contributionCalendar"]["totalContributions"], "last 12 months", CYAN),
        ("COMMITS", cc["totalCommitContributions"] + cc["restrictedContributionsCount"], "last 12 months", MAGENTA),
        ("PULL REQUESTS", u["pullRequests"]["totalCount"], "all time", YELLOW),
        ("PUBLIC REPOS", u["repositories"]["totalCount"], "original work", PURPLE),
        ("ACTIVE DAYS", active, "last 12 months", GREEN),
    ]
    W, H = 1000, 150
    tw = (W - 48 - 4 * 12) / 5
    out = [f'<text class="h" x="24" y="32">// GITHUB TELEMETRY · @{escape(LOGIN)} · UPDATED {date.today():%d %b %Y}</text>']
    for i, (k, v, sub, c) in enumerate(tiles):
        x = 24 + i * (tw + 12)
        out.append(f'''<g style="animation:up .7s {i * .12:.2f}s cubic-bezier(.2,.8,.2,1) both">
<rect x="{x:.1f}" y="48" width="{tw:.1f}" height="80" rx="10" fill="#0f0f24" stroke="{EDGE}"/>
<rect x="{x:.1f}" y="48" width="{tw:.1f}" height="2" fill="{c}"/>
<text x="{x + 16:.1f}" y="70" style="font:700 10.5px {MONO};letter-spacing:1.5px;fill:{MUTED}">{k}</text>
<text x="{x + 16:.1f}" y="104" style="font:800 30px {MONO};fill:{c}" filter="url(#g)">{fmt(v)}</text>
<text x="{x + 16:.1f}" y="120" style="font:500 10.5px {MONO};fill:{MUTED}">{sub}</text></g>''')
    return frame(W, H, "".join(out))


def languages_svg(u):
    sizes = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            if n not in SKIP_LANGS:
                sizes[n] = sizes.get(n, 0) + e["size"]
    total = sum(sizes.values()) or 1
    top = sorted(sizes.items(), key=lambda kv: -kv[1])[:6]
    W, H = 490, 60 + 34 * max(len(top), 1) + 6
    out = ['<text class="h" x="24" y="32">// TOP LANGUAGES · BY CODE SIZE</text>']
    for i, (name, s) in enumerate(top):
        pct = s / total * 100
        y = 58 + i * 34
        c = LANG_COLORS[i % len(LANG_COLORS)]
        bw = (W - 48) * pct / 100
        out.append(f'''<text x="24" y="{y + 10}" style="font:600 13px {MONO};fill:{TEXT}">{escape(name)}</text>
<text x="{W - 24}" y="{y + 10}" text-anchor="end" style="font:700 12px {MONO};fill:{c}">{pct:.1f}%</text>
<rect x="24" y="{y + 17}" width="{W - 48}" height="6" rx="3" fill="#15152e"/>
<rect x="24" y="{y + 17}" width="{max(bw, 4):.1f}" height="6" rx="3" fill="{c}" filter="url(#g)"
 style="transform-box:fill-box;transform-origin:left;animation:grow 1.2s {0.2 + i * .12:.2f}s cubic-bezier(.2,.8,.2,1) both"/>''')
    return frame(W, H, "".join(out), "@keyframes grow { from {transform:scaleX(0)} to {transform:scaleX(1)} }")


def activity_svg(u):
    days = [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]][-60:]
    W, H = 1000, 280
    L, R, T, B = 56, 24, 56, 44
    mx = max([d["contributionCount"] for d in days] + [4])
    pw, ph = W - L - R, H - T - B

    def xy(i, v):
        return L + pw * i / (len(days) - 1), T + ph - ph * v / mx

    pts = [xy(i, d["contributionCount"]) for i, d in enumerate(days)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{L},{T + ph} " + line + f" {L + pw},{T + ph}"
    grid = "".join(
        f'<line x1="{L}" x2="{W - R}" y1="{T + ph - ph * k / 4:.1f}" y2="{T + ph - ph * k / 4:.1f}" stroke="#ffffff" stroke-opacity=".06"/>'
        f'<text x="{L - 10}" y="{T + ph - ph * k / 4 + 4:.1f}" text-anchor="end" style="font:500 10px {MONO};fill:{MUTED}">{round(mx * k / 4)}</text>'
        for k in range(5))
    labels = "".join(
        f'<text x="{pts[i][0]:.1f}" y="{H - 18}" text-anchor="middle" style="font:500 10px {MONO};fill:{MUTED}">{date.fromisoformat(days[i]["date"]):%d %b}</text>'
        for i in range(0, len(days), 7))
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{MAGENTA}" style="animation:pop .4s {1.6 + i * .02:.2f}s both"/>'
        for i, (x, y) in enumerate(pts) if days[i]["contributionCount"] > 0)
    total = sum(d["contributionCount"] for d in days)
    defs = (f'<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>')
    css = (".ln { stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 2s cubic-bezier(.4,0,.2,1) forwards; }"
           "@keyframes draw { to { stroke-dashoffset: 0 } }"
           ".ar { animation: fade 1.2s .8s both } @keyframes fade { from {opacity:0} to {opacity:1} }"
           "@keyframes pop { from {opacity:0;r:0} to {opacity:1;r:3} }")
    inner = (f'<text class="h" x="24" y="32">// CONTRIBUTION ACTIVITY · LAST 60 DAYS · {total} CONTRIBUTIONS</text>'
             f'{grid}{labels}<polygon class="ar" points="{area}" fill="url(#area)"/>'
             f'<polyline class="ln" points="{line}" fill="none" stroke="{CYAN}" stroke-width="2.5" stroke-linejoin="round" pathLength="1" filter="url(#g)"/>{dots}')
    return frame(W, H, inner, css, defs)


if __name__ == "__main__":
    u = gql()
    for name, fn in [("stats.svg", stats_svg), ("languages.svg", languages_svg), ("activity.svg", activity_svg)]:
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(fn(u))
        print("wrote", os.path.join(OUT, name))
