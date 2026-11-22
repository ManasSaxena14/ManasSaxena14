#!/usr/bin/env python3
"""Self-hosted GitHub stats in the portfolio palette (no third-party stats service needed).

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

PANEL, EDGE, SOFT_EDGE, TRACK = "#111113", "#27272a", "#1e1e22", "#18181b"
ACCENT = "#c8f25a"
TEXT, SOFT, MUTED, DIM = "#fafafa", "#c4c4cc", "#a1a1aa", "#8b8b94"
SANS = "'Inter', 'Geist', 'Helvetica Neue', 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
SKIP_LANGS = {"Jupyter Notebook", "HTML", "CSS", "SCSS", "Shell", "Dockerfile", "Makefile", "Procfile", "Batchfile"}
LANG_COLORS = [ACCENT, "#d4d4d8", "#a1a1aa", "#8b8b94", "#71717a", "#52525b"]

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


def frame(W, H, inner, extra_css="", defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><clipPath id="clip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16"/></clipPath>{defs}</defs>
<style><![CDATA[
.h {{ font: 500 11px {MONO}; letter-spacing: 1.6px; fill: {DIM}; }}
.h tspan {{ fill: {ACCENT}; }}
@keyframes up {{ from {{opacity:0;transform:translateY(8px)}} to {{opacity:1;transform:none}} }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
{extra_css}
]]></style>
<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="{PANEL}"/>{inner}</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{EDGE}"/>
</svg>'''


def fmt(n):
    return f"{n / 1000:.1f}k" if n >= 10000 else f"{n:,}"


def stats_svg(u):
    cc = u["contributionsCollection"]
    active = sum(1 for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"] if d["contributionCount"] > 0)
    tiles = [
        ("CONTRIBUTIONS", cc["contributionCalendar"]["totalContributions"], "last 12 months", ACCENT),
        ("COMMITS", cc["totalCommitContributions"] + cc["restrictedContributionsCount"], "last 12 months", TEXT),
        ("PULL REQUESTS", u["pullRequests"]["totalCount"], "all time", TEXT),
        ("PUBLIC REPOS", u["repositories"]["totalCount"], "original work", TEXT),
        ("ACTIVE DAYS", active, "last 12 months", TEXT),
    ]
    W, H = 1000, 160
    tw = (W - 56) / 5
    out = [f'<text class="h" x="28" y="36"><tspan>●</tspan>  GITHUB · @{escape(LOGIN).upper()} · UPDATED {date.today():%d %b %Y}</text>',
           f'<line x1="28" y1="54" x2="{W - 28}" y2="54" stroke="{SOFT_EDGE}"/>']
    for i, (k, v, sub, c) in enumerate(tiles):
        x = 28 + i * tw
        pad = 0 if i == 0 else 20
        if i:
            out.append(f'<line x1="{x:.1f}" y1="70" x2="{x:.1f}" y2="136" stroke="{SOFT_EDGE}"/>')
        out.append(f'''<g>
<text x="{x + pad:.1f}" y="98" style="font:600 32px {SANS};letter-spacing:-1px;fill:{c}">{fmt(v)}</text>
<text x="{x + pad:.1f}" y="118" style="font:500 10.5px {MONO};letter-spacing:1.4px;fill:{SOFT}">{k}</text>
<text x="{x + pad:.1f}" y="134" style="font:400 11px {SANS};fill:{DIM}">{sub}</text></g>''')
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
    W, H = 490, 62 + 34 * max(len(top), 1) + 10
    out = ['<text class="h" x="28" y="36"><tspan>●</tspan>  TOP LANGUAGES · BY CODE SIZE</text>']
    for i, (name, s) in enumerate(top):
        pct = s / total * 100
        y = 62 + i * 34
        c = LANG_COLORS[i % len(LANG_COLORS)]
        bw = (W - 56) * pct / 100
        out.append(f'''<text x="28" y="{y + 10}" style="font:500 13.5px {SANS};fill:{TEXT}">{escape(name)}</text>
<text x="{W - 28}" y="{y + 10}" text-anchor="end" style="font:500 12px {MONO};fill:{SOFT}">{pct:.1f}%</text>
<rect x="28" y="{y + 18}" width="{W - 56}" height="4" rx="2" fill="{TRACK}"/>
<rect x="28" y="{y + 18}" width="{max(bw, 4):.1f}" height="4" rx="2" fill="{c}"/>''')
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
        f'<line x1="{L}" x2="{W - R}" y1="{T + ph - ph * k / 4:.1f}" y2="{T + ph - ph * k / 4:.1f}" stroke="#ffffff" stroke-opacity=".05"/>'
        f'<text x="{L - 10}" y="{T + ph - ph * k / 4 + 4:.1f}" text-anchor="end" style="font:500 10px {MONO};fill:{MUTED}">{round(mx * k / 4)}</text>'
        for k in range(5))
    labels = "".join(
        f'<text x="{pts[i][0]:.1f}" y="{H - 18}" text-anchor="middle" style="font:500 10px {MONO};fill:{MUTED}">{date.fromisoformat(days[i]["date"]):%d %b}</text>'
        for i in range(0, len(days), 7))
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{ACCENT}"/>'
        for i, (x, y) in enumerate(pts) if days[i]["contributionCount"] > 0)
    total = sum(d["contributionCount"] for d in days)
    defs = (f'<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".16"/>'
            f'<stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient>')
    css = (""
           "@keyframes draw { to { stroke-dashoffset: 0 } }"
           ""
           "@keyframes pop { from {opacity:0;r:0} to {opacity:1;r:2.5} }")
    inner = (f'<text class="h" x="28" y="36"><tspan>●</tspan>  CONTRIBUTION ACTIVITY · LAST 60 DAYS · {total} CONTRIBUTIONS</text>'
             f'{grid}{labels}<polygon class="ar" points="{area}" fill="url(#area)"/>'
             f'<polyline class="ln" points="{line}" fill="none" stroke="{ACCENT}" stroke-width="2" stroke-linejoin="round" pathLength="1"/>{dots}')
    return frame(W, H, inner, css, defs)


if __name__ == "__main__":
    u = gql()
    for name, fn in [("stats.svg", stats_svg), ("languages.svg", languages_svg), ("activity.svg", activity_svg)]:
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(fn(u))
        print("wrote", os.path.join(OUT, name))
