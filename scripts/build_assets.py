#!/usr/bin/env python3
"""Generate the animated SVGs used by README.md (dark and light copies of the infographics,
one dark copy of the clickable buttons and project covers).

    python3 scripts/build_assets.py

Everything is plain SVG + CSS: no scripts, no external fonts or images, so the
files animate when GitHub serves them through <img>. Edit the data blocks
(PHRASES, METRICS, ROWS, MILESTONES, STACK, SECTIONS) and re-run to update the visuals.
Tech icons in icons.json come from Simple Icons (CC0).
"""
import json
import math
import random
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
ICONS = json.loads((Path(__file__).parent / "icons.json").read_text())

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(
        card1="#111a27", card2="#0d1117", surface="#161b22", chip="#0d1117", border="#30363d",
        text="#f0f6fc", body="#c9d1d9", muted="#8b949e", faint="#3d444d", edge="#6e7681",
        a1="#34d399", a2="#22d3ee", a3="#a78bfa", a4="#fbbf24", g1="#34d399", g2="#22d3ee",
        ok="#3fb950", merged="#a371f7", err="#f85149", node="#0d1117", glowop="0.24", sheenop="0.16",
        onaccent="#04130d",
    ),
    "light": dict(
        card1="#ffffff", card2="#eef5f6", surface="#f6f8fa", chip="#ffffff", border="#d0d7de",
        text="#1f2328", body="#3b434b", muted="#59636e", faint="#c3ccd5", edge="#8c959f",
        a1="#047857", a2="#0e7490", a3="#6d28d9", a4="#b45309", g1="#10b981", g2="#06b6d4",
        ok="#1a7f37", merged="#8250df", err="#cf222e", node="#ffffff", glowop="0.20", sheenop="0.45",
        onaccent="#04130d",
    ),
}

# ── content ────────────────────────────────────────────────────────────────
NAME = "G O Ashwin Praveen"
HANDLE = "ashwin.praveen"
STATUS = "Available for SWE roles · 2027 grad"
LOCATION = "Kannur, Kerala, India"

# (keyword, rest) — typed in the hero, one after another
PHRASES = [
    ("full-stack", "Django, GraphQL, React"),
    ("mobile", "Flutter app, 1,000+ downloads"),
    ("open source", "14 PRs merged upstream"),
    ("systems", "RL autoscaling on Kubernetes"),
]

# (number, suffix, label, sub-label, colour key, icon)
METRICS = [
    ("1,000+", "", "App downloads", "Priyamvada · Flutter", "a1", "download"),
    ("14", "", "PRs merged upstream", "CARE · Scribe-Android", "merged", "merge"),
    ("2", "", "Internships", "Traboda · Pupilfirst", "a2", "briefcase"),
    ("2×", "", "Hackathon honors", "Runner-up · Finalist", "a4", "trophy"),
]

NOW = 2026.87  # Nov 2026 — where the "now" marker sits on the timeline
# (title, sub, start, end, colour key, label inside/after the bar)
ROWS = [
    ("B.Tech CSE · Amrita", "Undergrad · Amritapuri campus", 2023.60, 2027.40, "a3", "2023 – 2027"),
    ("Traboda CyberLabs", "Software Developer Intern", 2024.08, 2025.42, "a2", "Feb 2024 – May 2025"),
    ("Pupilfirst", "Jr. Full Stack Engineer Intern", 2025.08, 2025.67, "a4", "Feb – Aug 2025"),
    ("CIR Skill Platform", "Team Lead · Django + GraphQL", 2025.25, NOW, "a1", "Apr 2025 – present"),
]
# (when, label, colour key, above the axis?)
MILESTONES = [
    (2024.79, "Evolumin finalist", "a4", True),
    (2025.20, "OLabs runner-up", "a4", False),
    (2025.54, "Wikimedia hackathon", "a2", True),
    (2025.87, "CampusNotes+", "a1", False),
    (2026.80, "FlexaScale", "a1", True),
]

# (group, [(label, icon slug, dark colour, light colour)])
STACK = [
    ("Languages", [
        ("Python", "python", "#5a9fd4", "#3776ab"), ("Java", "openjdk", "#e0913a", "#b8651b"),
        ("Dart", "dart", "#40c4ff", "#0175c2"), ("JavaScript", "javascript", "#f7df1e", "#c9a800"),
        ("TypeScript", "typescript", "#4c9ae6", "#3178c6"), ("Kotlin", "kotlin", "#a68bff", "#7f52ff"),
    ]),
    ("Frameworks", [
        ("Flutter", "flutter", "#54c5f8", "#02569b"), ("React", "react", "#61dafb", "#149eca"),
        ("Next.js", "nextdotjs", "#f0f6fc", "#1f2328"), ("Django", "django", "#44b78b", "#0c4b33"),
        ("Node.js", "nodedotjs", "#6cc24a", "#3c873a"),
    ]),
    ("APIs & data", [
        ("GraphQL", "graphql", "#f25cc1", "#e10098"), ("Firebase", "firebase", "#ffa000", "#dd2c00"),
        ("PostgreSQL", "postgresql", "#6b9cf0", "#336791"), ("MySQL", "mysql", "#5d9cc9", "#00618a"),
    ]),
    ("Infra & tools", [
        ("Docker", "docker", "#2496ed", "#1d7fc9"), ("Kubernetes", "kubernetes", "#5b8def", "#326ce5"),
        ("Git", "git", "#f05032", "#de4c36"), ("Linux", "linux", "#fcc624", "#1f2328"),
        ("Figma", "figma", "#f24e1e", "#f24e1e"),
    ]),
]

# (repo, sub-label, colour key, merged PR numbers in order)
OSS = [
    ("ohcnetwork/care_fe", "CARE · healthcare DPG · 10 merged", "a1",
     [9410, 10298, 10655, 10773, 10802, 11238, 12304, 12383, 12388, 13037]),
    ("scribe-org/Scribe-Android", "Wikimedia hackathon · 4 merged", "a2", [445, 450, 457, 462]),
]

# slug: (name, tag, colour key, motif)
COVERS = {
    "skill-platform": ("Skill Development Platform", "TEAM LEAD · LIVE IN PRODUCTION", "a1", "bars"),
    "flexascale": ("FlexaScale", "RL AUTOSCALER · KUBERNETES", "a2", "pods"),
    "colaba-ai": ("Colaba AI", "RUNNER-UP · OLABS HACKATHON 2025", "a3", "chat"),
    "campusnotes": ("CampusNotes+", "FLUTTER · FIREBASE · RAZORPAY", "a4", "notes"),
}

# (file slug, label, width, icon key, primary?)
BUTTONS = [
    ("portfolio", "Portfolio", 124, "globe", True),
    ("resume", "Résumé", 114, "doc", False),
    ("linkedin", "LinkedIn", 118, "in", False),
    ("email", "Email", 98, "mail", False),
    ("gitlab", "GitLab", 104, "gitlab", False),
]

# (file slug, title, tag shown on the right) — the animated section headings, numbered in order
SECTIONS = [
    ("experience", "Experience", "2 internships · 1 team lead role"),
    ("opensource", "Open source", "14 PRs merged upstream"),
    ("projects", "Selected projects", "4 builds · 1 live in production"),
    ("stack", "Stack", "20 tools I ship with"),
    ("honors", "Honors and community", "runner-up · finalist · mentor"),
    ("education", "Education", "B.Tech CSE · class of 2027"),
]


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def n(v):
    """Compact number formatting for coordinates."""
    return f"{v:.2f}".rstrip("0").rstrip(".")


def kf(name, T, stops):
    """@keyframes for a loop of T seconds, from (seconds, declarations) pairs."""
    return f"@keyframes {name}{{" + "".join(f"{n(s / T * 100)}%{{{css}}}" for s, css in stops) + "}"


def doc(w, h, label, css, defs, body, t):
    tpl = Template(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 $w $h" width="$w" height="$h" '
        'role="img" aria-label="$label">\n<title>$label</title>\n<style>\n'
        "text{font-family:$font}\n.mono,.mono text{font-family:$mono}\n$css\n"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}\n"
        "</style>\n<defs>\n$defs\n</defs>\n$body\n</svg>\n"
    )
    css = Template(css).substitute(t)
    defs = Template(defs).substitute(t)
    body = Template(body).substitute(t)
    return tpl.substitute(w=w, h=h, label=esc(label), font=FONT, mono=MONO, css=css, defs=defs, body=body)


SHARED_CSS = """
.up{animation:up .7s cubic-bezier(.22,1,.36,1) both}
@keyframes up{from{opacity:0;transform:translateY(10px)}}
.fade{animation:fade .8s ease-out both}
@keyframes fade{from{opacity:0}}
.pop{transform-box:fill-box;transform-origin:center;animation:pop .6s cubic-bezier(.34,1.56,.64,1) both}
@keyframes pop{from{transform:scale(0);opacity:0}}
.ring{fill:none;stroke-width:1.5;opacity:0;transform-box:fill-box;transform-origin:center;animation:ring 3s ease-out infinite}
@keyframes ring{0%{transform:scale(1);opacity:.75}100%{transform:scale(3.4);opacity:0}}
@keyframes hit{0%{transform:scale(1);opacity:.9}14%{transform:scale(3);opacity:0}100%{transform:scale(3);opacity:0}}
.tw{transform-box:fill-box;transform-origin:center;animation:tw 2.8s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.15;transform:scale(.45)}50%{opacity:1;transform:scale(1)}}
.beam{fill:none;stroke-width:1.5;stroke-linecap:round;stroke-dasharray:14 86;animation:beam 8s linear infinite}
@keyframes beam{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}
.blink{animation:blink 1.1s step-end infinite}
@keyframes blink{0%{opacity:1}55%{opacity:0}100%{opacity:0}}
"""

SPARK = "M0-5L1.2-1.2 5 0 1.2 1.2 0 5-1.2 1.2-5 0-1.2-1.2Z"  # four-point twinkle
HUB = ('<linearGradient id="hub" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$g1"/>'
       '<stop offset="1" stop-color="$g2"/></linearGradient>')
# the arcade ship, nose up at (0, -14); reused as a flyby in the headings and footer (needs HUB)
SHIP = ('<g id="ship"><path d="M0-14L12 8 4 5 0 9-4 5-12 8Z" fill="url(#hub)"/>'
        '<circle cy="-2" r="2.6" fill="$node"/></g>')


# ── hero ───────────────────────────────────────────────────────────────────
def hero(t):
    W, H = 840, 300
    nodes = [(676, 150, 9), (580, 92, 5), (608, 214, 5), (752, 72, 6), (790, 168, 5), (726, 244, 4.5),
             (530, 170, 4), (648, 52, 4), (814, 98, 3.5), (552, 250, 3.5), (818, 236, 3.5)]
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 6), (1, 7), (3, 7), (3, 8), (4, 8),
             (4, 10), (5, 10), (2, 9), (6, 9), (2, 6), (2, 5), (4, 5)]
    # (from, to, delay, reversed) — dots that travel along an edge
    packets = [(0, 1, 0.0, False), (0, 3, 1.1, False), (0, 4, 2.3, True), (0, 2, 0.7, True),
               (0, 5, 3.1, False), (0, 6, 1.8, True), (3, 8, 2.8, False), (2, 9, 3.6, False),
               (1, 7, 4.2, True), (4, 10, 0.4, False)]
    # (glyph, x, y) — code tokens that drift up through the background
    tokens = [("</>", 452, 74), ("{ }", 488, 266), ("=>", 604, 286), ("λ", 806, 282), ("()", 770, 28),
              ("&&", 446, 198), ("#!", 540, 30), ("[ ]", 818, 132)]

    def seg(a, b):
        return f"M{nodes[a][0]} {nodes[a][1]}L{nodes[b][0]} {nodes[b][1]}"

    mesh = []
    for i, (a, b) in enumerate(edges):
        mesh.append(f'<path class="e" style="animation-delay:{0.3 + i * 0.06:.2f}s" pathLength="1" d="{seg(a, b)}"/>')
    for a, b, delay, rev in packets:
        style = f"animation-delay:{delay + 1.6:.1f}s" + (";animation-direction:reverse" if rev else "")
        mesh.append(f'<path class="pk" style="{style}" pathLength="1" d="{seg(a, b)}"/>')
    hx, hy, hr = nodes[0]
    mesh.append(f'<circle class="ring" stroke="$g1" cx="{hx}" cy="{hy}" r="{hr}"/>')
    mesh.append(f'<circle class="ring" stroke="$g2" style="animation-delay:1.5s" cx="{hx}" cy="{hy}" r="{hr}"/>')
    # two orbits around the hub; the unfilled outer circle keeps each group's box centred on the hub
    mesh.append(
        f'<g class="fade" style="animation-delay:1.3s">'
        f'<g class="orb"><circle cx="{hx}" cy="{hy}" r="34" fill="none"/><circle cx="{hx}" cy="{hy}" r="28" fill="none" '
        f'stroke="$g1" stroke-opacity=".5" stroke-dasharray="2 5"/><circle cx="{hx + 28}" cy="{hy}" r="2.6" fill="$g1"/></g>'
        f'<g class="orb" style="animation-duration:26s;animation-direction:reverse"><circle cx="{hx}" cy="{hy}" r="50" '
        f'fill="none"/><circle cx="{hx}" cy="{hy}" r="46" fill="none" stroke="$g2" stroke-opacity=".35" '
        f'stroke-dasharray="1 8"/><circle cx="{hx}" cy="{hy - 46}" r="2.2" fill="$g2"/></g></g>')
    for i, (x, y, r) in enumerate(nodes):
        delay = f"animation-delay:{0.5 + i * 0.07:.2f}s"
        if i == 0:
            mesh.append(f'<g class="pop" style="{delay}"><circle cx="{x}" cy="{y}" r="{r + 6}" fill="none" '
                        f'stroke="$g1" stroke-opacity=".35"/><circle cx="{x}" cy="{y}" r="{r}" fill="url(#hub)"/>'
                        f'<circle cx="{x}" cy="{y}" r="3" fill="$node"/></g>')
        else:
            stroke = "$g2" if i % 2 else "$g1"
            mesh.append(f'<circle class="pop nd" style="{delay}" stroke="{stroke}" cx="{x}" cy="{y}" r="{r}"/>')

    # a sky of twinkling stars, kept out of the text block
    rnd = random.Random(5)
    sky = []
    while len(sky) < 26:
        x, y = rnd.uniform(14, 826), rnd.uniform(12, 288)
        if 30 < x < 640 and 56 < y < 256:
            continue
        timing = f"animation-duration:{rnd.uniform(2.2, 4.6):.1f}s;animation-delay:{-rnd.uniform(0, 4):.1f}s"
        if len(sky) % 6 == 0:
            sky.append(f'<g transform="translate({n(x)} {n(y)}) scale(.8)"><path class="tw" style="{timing}" d="{SPARK}" '
                       f'fill="{"$g2" if len(sky) % 12 else "$g1"}"/></g>')
        else:
            sky.append(f'<circle class="tw" style="{timing}" cx="{n(x)}" cy="{n(y)}" r="{rnd.choice((.8, 1, 1.3))}" fill="$muted"/>')
    code = "".join(f'<text class="cg mono" style="animation-delay:{-i * 1.7:.1f}s" x="{x}" y="{y}" font-size="13" '
                   f'fill="$muted" text-anchor="middle">{esc(g)}</text>' for i, (g, x, y) in enumerate(tokens))

    # typed line
    ADV, X0, Y, DT, SLOT, FADE = 9.0, 70, 182, 0.045, 4.6, 0.3
    T = SLOT * len(PHRASES)
    vis = SLOT - 0.4
    typed, kfs = [], []
    for j, (kw, rest) in enumerate(PHRASES):
        s = f"{kw} · {rest}"
        start = j * SLOT
        gdelay = start - T if j else 0
        chars = []
        for i, ch in enumerate(s):
            if ch == " ":
                continue
            cls = "c k" if i < len(kw) else "c"
            chars.append(f'<text class="{cls}" x="{n(X0 + i * ADV)}" y="{Y}" '
                         f'style="animation-delay:{start + i * DT - T:.3f}s">{esc(ch)}</text>')
        width = len(s) * ADV
        kfs.append(f"@keyframes cur{j}{{0%{{transform:translateX(0);animation-timing-function:steps({len(s)},start)}}"
                   f"{len(s) * DT / T * 100:.3f}%{{transform:translateX({n(width)}px)}}"
                   f"100%{{transform:translateX({n(width)}px)}}}}")
        typed.append(
            f'<g class="ph" style="opacity:{0 if j else 1};animation-delay:{gdelay:.2f}s">{"".join(chars)}'
            f'<g style="animation:cur{j} {n(T)}s linear {gdelay:.2f}s infinite">'
            f'<rect class="blink" fill="$a1" x="{X0 + 2}" y="{Y - 13}" width="8" height="16" rx="1.5"/></g></g>')
    a, b = (vis - FADE) / T * 100, vis / T * 100

    css = SHARED_CSS + f"""
.e{{fill:none;stroke:$edge;stroke-opacity:.55;stroke-width:1;stroke-dasharray:1;animation:draw 1.1s ease-out both}}
@keyframes draw{{from{{stroke-dashoffset:1}}}}
.pk{{fill:none;stroke:$g2;stroke-width:3.4;stroke-linecap:round;stroke-dasharray:.001 2;opacity:0;animation:flow 5.5s linear infinite}}
@keyframes flow{{0%{{stroke-dashoffset:2.001;opacity:0}}5%{{opacity:1}}31%{{opacity:1}}36%{{stroke-dashoffset:1.001;opacity:0}}100%{{stroke-dashoffset:1.001;opacity:0}}}}
.nd{{fill:$node;stroke-width:1.5}}
.float{{animation:float 9s ease-in-out infinite}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
.orb{{transform-box:fill-box;transform-origin:center;animation:spin 16s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.d1{{animation:drift 14s ease-in-out infinite}}
.d2{{animation:drift 17s ease-in-out infinite reverse}}
@keyframes drift{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-26px,16px)}}}}
.cg{{opacity:0;animation:cg 13.6s ease-in-out infinite}}
@keyframes cg{{0%{{opacity:0;transform:translateY(10px)}}20%,45%{{opacity:.5}}65%,100%{{opacity:0;transform:translateY(-16px)}}}}
.sheen{{opacity:0;animation:sheen 7s ease-in-out 1.4s infinite}}
@keyframes sheen{{0%{{transform:translateX(0);opacity:0}}6%{{opacity:1}}26%{{transform:translateX(580px);opacity:1}}30%,100%{{transform:translateX(580px);opacity:0}}}}
.gx1,.gx2{{opacity:0;animation:gx1 6.5s step-end 2.6s infinite}}
.gx2{{animation-name:gx2}}
@keyframes gx1{{0%{{opacity:0}}88%{{opacity:.9;transform:translate(-3px,1px)}}90%{{transform:translate(2px,-1px)}}92%{{transform:translate(-2px,0)}}94%{{opacity:0;transform:translate(0,0)}}}}
@keyframes gx2{{0%{{opacity:0}}88%{{opacity:.9;transform:translate(3px,-1px)}}90%{{transform:translate(-2px,1px)}}92%{{transform:translate(2px,0)}}94%{{opacity:0;transform:translate(0,0)}}}}
.c{{fill:$body;animation:ch {n(T)}s step-end infinite}}
.k{{fill:$a1}}
@keyframes ch{{0%{{opacity:1}}50%{{opacity:0}}100%{{opacity:0}}}}
.ph{{animation:ph {n(T)}s linear infinite}}
@keyframes ph{{0%{{opacity:1}}{a:.3f}%{{opacity:1}}{b:.3f}%{{opacity:0}}100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.blink{{display:none}}}}
""" + "\n".join(kfs)

    name = f'x="46" y="138" font-size="44" font-weight="800" letter-spacing="-.6"'
    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$card1"/><stop offset="1" stop-color="$card2"/></linearGradient>
<radialGradient id="ga"><stop offset="0" stop-color="$g1" stop-opacity="$glowop"/><stop offset="1" stop-color="$g1" stop-opacity="0"/></radialGradient>
<radialGradient id="gb"><stop offset="0" stop-color="$g2" stop-opacity="$glowop"/><stop offset="1" stop-color="$g2" stop-opacity="0"/></radialGradient>
{HUB}
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="$g1" stop-opacity="0"/><stop offset=".5" stop-color="$g2"/><stop offset="1" stop-color="$g1" stop-opacity="0"/></linearGradient>
<linearGradient id="fd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".45" stop-color="#fff"/></linearGradient>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="$faint"/></pattern>
<mask id="dm"><rect x="400" width="440" height="{H}" fill="url(#fd)"/></mask>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<clipPath id="nm"><text {name}>{esc(NAME)}</text></clipPath>
"""
    body = f"""
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<g clip-path="url(#card)">
<circle class="d1" cx="720" cy="20" r="270" fill="url(#ga)"/>
<circle class="d2" cx="90" cy="330" r="250" fill="url(#gb)"/>
<rect x="400" width="440" height="{H}" fill="url(#dots)" mask="url(#dm)" opacity=".7"/>
{"".join(sky)}
{code}
<g class="float">{"".join(mesh)}</g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="$border"/>
<rect class="beam" stroke="url(#hub)" pathLength="100" x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="17.25"/>
<g class="up" style="animation-delay:.05s"><text class="mono" x="48" y="84" font-size="13" letter-spacing=".4" fill="$a1">{esc(HANDLE)}<tspan fill="$muted">()</tspan></text></g>
<g class="up" style="animation-delay:.15s"><text class="gx1" {name} fill="$g1">{esc(NAME)}</text><text class="gx2" {name} fill="$a3">{esc(NAME)}</text><g clip-path="url(#nm)"><rect x="36" y="94" width="560" height="60" fill="$text"/><g transform="skewX(-18)"><rect class="sheen" x="10" y="88" width="90" height="72" fill="url(#sh)"/></g></g></g>
<g class="up mono" style="animation-delay:.3s" font-size="15"><path d="M49 {Y - 10}l6 5-6 5" fill="none" stroke="$a1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>{"".join(typed)}</g>
<g class="up" style="animation-delay:.45s"><rect x="48" y="212" width="292" height="32" rx="16" fill="$surface" fill-opacity=".75" stroke="$border"/><circle class="ring" stroke="$ok" style="animation-duration:2.4s" cx="67" cy="228" r="4"/><circle cx="67" cy="228" r="4" fill="$ok"/><text x="82" y="232.5" font-size="13" font-weight="600" fill="$text">{esc(STATUS)}</text><text x="356" y="232.5" font-size="12.5" fill="$muted">{esc(LOCATION)}</text></g>
"""
    label = f"{NAME} — software engineer, full-stack and mobile. {STATUS}. {LOCATION}."
    return doc(W, H, label, css, defs, body, t)


# ── metrics ────────────────────────────────────────────────────────────────
# 20×20 icons drawn in the tile colour ({c}); each carries its own small loop
METRIC_ICONS = {
    "download": ('<path d="M3 13.5v2.5c0 .8.7 1.5 1.5 1.5h11c.8 0 1.5-.7 1.5-1.5v-2.5"/>'
                 '<g class="dl"><path d="M10 2.5v10M5.8 8.6l4.2 4.2 4.2-4.2"/></g>'),
    "merge": ('<circle cx="5.5" cy="4.5" r="2.2"/><circle cx="5.5" cy="15.5" r="2.2"/><circle cx="14.5" cy="10" r="2.2"/>'
              '<path d="M5.5 6.7v6.6M5.5 6.7c0 3.3 3 3.3 6.8 3.3"/>'
              '<path class="fw" pathLength="1" d="M5.5 6.7c0 3.3 3 3.3 6.8 3.3"/>'
              '<circle class="ring" style="animation:hit 2.4s ease-out 1.6s infinite" cx="14.5" cy="10" r="2.2"/>'),
    "briefcase": ('<g class="sw"><rect x="2.5" y="6" width="15" height="11" rx="2"/>'
                  '<path d="M7.5 6V4.4c0-.8.6-1.4 1.4-1.4h2.2c.8 0 1.4.6 1.4 1.4V6M2.5 10.8h15"/>'
                  '<rect x="8.6" y="9.6" width="2.8" height="2.4" rx=".6" fill="{c}" stroke="none"/></g>'),
    "trophy": ('<g class="hop"><path d="M6 3h8v5a4 4 0 0 1-8 0z" fill="{c}" fill-opacity=".2"/>'
               '<path d="M6 4.5H3.5a2.5 2.5 0 0 0 2.6 3.9M14 4.5h2.5a2.5 2.5 0 0 1-2.6 3.9M10 12v3M6.5 17h7"/></g>'
               '<g transform="translate(18 2) scale(.5)"><path class="tw" d="{spark}" fill="{c}" stroke="none"/></g>'
               '<g transform="translate(1.5 14) scale(.38)"><path class="tw" style="animation-delay:-1.4s" d="{spark}" '
               'fill="{c}" stroke="none"/></g>'),
}


def metrics(t):
    W, H, TW, GAP = 840, 124, 198, 16
    BASE, STEP, SIZE = 58, 42, 34
    cells = {".": 9, ",": 9, "+": 21, "×": 20}
    body, defs, kfs = [], [HUB], set()
    for i, (num, suffix, label, sub, key, icon) in enumerate(METRICS):
        x = i * (TW + GAP)
        col = f"${key}"
        geo = f'x="{x + .75}" y=".75" width="{TW - 1.5}" height="{H - 1.5}" rx="12"'
        defs.append(f'<clipPath id="c{i}"><rect x="{x}" y="{BASE - 33}" width="{TW}" height="{STEP}"/></clipPath>')
        out = [f'<rect {geo} fill="$surface" stroke="$border"/>',
               f'<rect class="beam" stroke="url(#hub)" style="animation-delay:{-i * 2:.2f}s" pathLength="100" {geo}/>']
        cx, digit, digits = x + 20, 0, []
        for ch in num:
            if ch.isdigit():
                d = int(ch)
                seq = list(range(10)) + list(range(d + 1))
                last = len(seq) - 1
                kfs.add(f"@keyframes r{last}{{from{{transform:translateY({last * STEP}px)}}}}")
                items = "".join(f'<text x="{n(cx + 10.75)}" y="{BASE + (k - last) * STEP}">{v}</text>'
                                for k, v in enumerate(seq))
                digits.append(f'<g class="roll" style="animation-name:r{last};'
                              f'animation-delay:{0.25 + i * 0.18 + digit * 0.12:.2f}s">{items}</g>')
                cx += 21.5
                digit += 1
            else:
                w = cells[ch]
                digits.append(f'<text class="fade" style="animation-delay:{0.9 + i * 0.18:.2f}s" '
                              f'x="{n(cx + w / 2)}" y="{BASE}">{esc(ch)}</text>')
                cx += w
        out.append(f'<g clip-path="url(#c{i})" font-size="{SIZE}" font-weight="800" fill="$text" '
                   f'text-anchor="middle">{"".join(digits)}</g>')
        if suffix:
            out.append(f'<text class="fade" style="animation-delay:{1.2 + i * 0.18:.2f}s" x="{n(cx + 5)}" y="{BASE}" '
                       f'font-size="15" font-weight="600" fill="$muted">{esc(suffix)}</text>')
        ix = x + TW - 42
        out.append(f'<rect x="{ix - 4}" y="14" width="28" height="28" rx="8" fill="{col}" fill-opacity=".12"/>'
                   f'<g transform="translate({ix} 18)" fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round" '
                   f'stroke-linejoin="round">{METRIC_ICONS[icon].format(c=col, spark=SPARK)}</g>')
        out.append(f'<text x="{x + 20}" y="88" font-size="13" font-weight="600" fill="$body">{esc(label)}</text>')
        out.append(f'<text x="{x + 20}" y="106" font-size="11.5" fill="$muted">{esc(sub)}</text>')
        body.append(f'<g class="up" style="animation-delay:{i * 0.1:.1f}s">{"".join(out)}</g>')
    css = SHARED_CSS + """
.roll{animation-duration:1.9s;animation-timing-function:cubic-bezier(.16,1,.3,1);animation-fill-mode:both}
.dl{animation:dl 1.8s cubic-bezier(.5,0,.5,1) infinite}
@keyframes dl{0%{transform:translateY(-4px);opacity:0}30%{opacity:1}60%{transform:translateY(1.5px);opacity:1}100%{transform:translateY(1.5px);opacity:0}}
.fw{stroke-width:3.2;stroke-dasharray:.001 2;opacity:0;animation:fw 2.4s ease-in-out infinite}
@keyframes fw{0%{stroke-dashoffset:2.001;opacity:0}10%{opacity:1}60%{opacity:1}67%{stroke-dashoffset:1.001;opacity:0}100%{stroke-dashoffset:1.001;opacity:0}}
.sw{transform-box:fill-box;transform-origin:50% 0;animation:sw 2.8s ease-in-out infinite}
@keyframes sw{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(8deg)}}
.hop{transform-box:fill-box;transform-origin:50% 100%;animation:hop 2.4s cubic-bezier(.3,0,.3,1) infinite}
@keyframes hop{0%,40%,100%{transform:translateY(0) scale(1)}20%{transform:translateY(-2.5px) scale(1.08)}}
""" + "\n".join(sorted(kfs))
    label = "At a glance: " + "; ".join(f"{num}{suf} {lab} ({sub})" for num, suf, lab, sub, _, _ in METRICS)
    return doc(W, H, label, css, "\n".join(defs), "\n".join(body), t)


# ── timeline ───────────────────────────────────────────────────────────────
def timeline(t):
    W, H = 840, 288
    X0, X1, T0, T1 = 218, 812, 2023.5, 2027.5
    AXIS = 248
    COMET, LOOP = 2.4, 8  # a comet runs along the milestone axis in the first 45% of each loop

    def X(year):
        return X0 + (year - T0) / (T1 - T0) * (X1 - X0)

    xn = X(NOW)
    body = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="$surface" stroke="$border"/>']
    for year in range(2024, 2028):
        x = n(X(year))
        body.append(f'<line x1="{x}" x2="{x}" y1="34" y2="{H - 18}" stroke="$border" stroke-dasharray="2 4"/>')
        body.append(f'<text class="mono" x="{x}" y="24" font-size="10.5" fill="$muted" text-anchor="middle">{year}</text>')
    defs = ['<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff" stop-opacity="$sheenop"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>']
    for i, (title, sub, start, end, key, tag) in enumerate(ROWS):
        cy = 64 + i * 44
        delay = 0.2 + i * 0.16
        col = f"${key}"
        body.append(f'<text x="24" y="{cy - 2}" font-size="12.5" font-weight="600" fill="$text">{esc(title)}</text>')
        body.append(f'<text x="24" y="{cy + 13}" font-size="11" fill="$muted">{esc(sub)}</text>')
        xs, solid_end = X(start), X(min(end, NOW))
        geo = f'x="{n(xs)}" y="{cy - 11}" width="{n(solid_end - xs)}" height="22" rx="6"'
        if end > NOW:  # the part that has not happened yet
            body.append(f'<rect class="fade" style="animation-delay:{delay + .7:.2f}s" x="{n(xn)}" y="{cy - 11}" '
                        f'width="{n(X(end) - xn)}" height="22" rx="6" fill="{col}" fill-opacity=".05" '
                        f'stroke="{col}" stroke-opacity=".55" stroke-dasharray="4 4"/>')
        body.append(f'<g class="grow" style="animation-delay:{delay:.2f}s"><rect {geo} fill="{col}" '
                    f'fill-opacity=".16" stroke="{col}" stroke-opacity=".75"/></g>')
        defs.append(f'<clipPath id="b{i}"><rect {geo}/></clipPath>')
        body.append(f'<g clip-path="url(#b{i})"><rect class="sweep" style="animation-delay:{1.5 + i * .5:.1f}s" '
                    f'x="{n(xs - 90)}" y="{cy - 11}" width="70" height="22" fill="url(#sw)"/></g>')
        inside = solid_end - xs > len(tag) * 6.6 + 20
        tx = xs + 10 if inside else solid_end + 9
        body.append(f'<text class="mono fade" style="animation-delay:{delay + .55:.2f}s" x="{n(tx)}" y="{cy + 3.5}" '
                    f'font-size="10.5" fill="{col}">{esc(tag)}</text>')
    # milestones, each pinged as the comet passes
    axis = f"M{X0} {AXIS}H{X1}"
    body.append(f'<text x="24" y="{AXIS - 2}" font-size="12.5" font-weight="600" fill="$text">Milestones</text>')
    body.append(f'<text x="24" y="{AXIS + 13}" font-size="11" fill="$muted">awards · hackathons · launches</text>')
    body.append(f'<line x1="{X0}" x2="{X1}" y1="{AXIS}" y2="{AXIS}" stroke="$faint"/>')
    body.append(f'<path class="ct" pathLength="1" d="{axis}"/><path class="ch" pathLength="1" d="{axis}"/>')
    for i, (when, label, key, above) in enumerate(MILESTONES):
        x, delay = n(X(when)), 1.0 + i * 0.14
        hit = COMET + (X(when) - X0) / (X1 - X0) * LOOP * .45
        body.append(f'<g transform="translate({x} {AXIS}) rotate(45)">'
                    f'<rect class="ring" stroke="${key}" style="animation:hit {LOOP}s ease-out {hit:.2f}s infinite" '
                    f'x="-4.5" y="-4.5" width="9" height="9" rx="1.5"/><rect class="pop" style="animation-delay:{delay:.2f}s" '
                    f'x="-4.5" y="-4.5" width="9" height="9" rx="1.5" fill="${key}"/></g>')
        body.append(f'<text class="fade" style="animation-delay:{delay + .15:.2f}s" x="{x}" y="{AXIS - 13 if above else AXIS + 22}" '
                    f'font-size="10.5" font-weight="600" fill="$body" text-anchor="middle">{esc(label)}</text>')
    # now marker
    body.append(f'<line class="ants" x1="{n(xn)}" x2="{n(xn)}" y1="40" y2="214" '
                f'stroke="$g1" stroke-width="1.2" stroke-dasharray="3 3"/>')
    body.append(f'<circle class="ring" stroke="$g1" cx="{n(xn)}" cy="40" r="3.5"/><circle cx="{n(xn)}" cy="40" r="3.5" fill="$g1"/>')
    body.append(f'<text class="mono" x="{n(xn - 12)}" y="43.5" font-size="10" fill="$a1" text-anchor="end">now</text>')
    css = SHARED_CSS + f"""
.grow{{transform-box:fill-box;transform-origin:left center;animation:grow 1s cubic-bezier(.22,1,.36,1) both}}
@keyframes grow{{from{{transform:scaleX(0)}}}}
.sweep{{opacity:0;animation:sweep 4.5s linear infinite}}
@keyframes sweep{{0%{{transform:translateX(0);opacity:1}}70%{{transform:translateX(720px);opacity:1}}71%,100%{{transform:translateX(720px);opacity:0}}}}
.ants{{animation:fade .8s ease-out 1.2s both,ants 1.2s linear infinite}}
@keyframes ants{{to{{stroke-dashoffset:-12}}}}
.ct,.ch{{fill:none;stroke:$g1;stroke-linecap:round;opacity:0;animation:ct {LOOP}s linear {COMET}s infinite}}
.ct{{stroke-opacity:.45;stroke-width:2.4;stroke-dasharray:.07 2}}
.ch{{stroke-width:5.5;stroke-dasharray:.001 2;animation-name:ch}}
@keyframes ct{{0%{{stroke-dashoffset:2.14;opacity:0}}3%{{opacity:1}}42%{{opacity:1}}45%{{stroke-dashoffset:1.14;opacity:0}}100%{{stroke-dashoffset:1.14;opacity:0}}}}
@keyframes ch{{0%{{stroke-dashoffset:2.001;opacity:0}}3%{{opacity:1}}42%{{opacity:1}}45%{{stroke-dashoffset:1.001;opacity:0}}100%{{stroke-dashoffset:1.001;opacity:0}}}}
"""
    label = ("Timeline 2023–2027. " + " ".join(f"{title}: {sub}, {tag}." for title, sub, _, _, _, tag in ROWS)
             + " Milestones: " + ", ".join(m[1] for m in MILESTONES) + ".")
    return doc(W, H, label, css, "\n".join(defs), "\n".join(body), t)


# ── stack ──────────────────────────────────────────────────────────────────
def stack(t, theme):
    W, ROW, CH = 840, 46, 34
    H = 22 + len(STACK) * ROW - (ROW - CH) + 22
    body = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="$surface" stroke="$border"/>']
    k = 0
    for r, (group, items) in enumerate(STACK):
        y = 22 + r * ROW
        body.append(f'<text class="mono" x="24" y="{y + 21}" font-size="10.5" letter-spacing="1.2" '
                    f'fill="$muted">{esc(group.upper())}</text>')
        x = 176
        for label, slug, dark, light in items:
            w = round(36 + len(label) * 7.6 + 14)
            colour = dark if theme == "dark" else light
            geo = f'x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{CH - 1}" rx="9"'
            spot = f"animation-delay:{1.4 + k * 0.13:.2f}s"  # the highlight and icon pop travel chip to chip
            body.append(
                f'<g class="up" style="animation-delay:{k * 0.05:.2f}s"><g class="bob" style="animation-delay:{k * .14 - 9:.2f}s">'
                f'<rect {geo} fill="$chip" stroke="$border"/><rect class="wave" style="{spot}" {geo}/>'
                f'<g transform="translate({x + 12} {y + 9}) scale({16 / 24:.4f})"><path class="ipop" style="{spot}" '
                f'fill="{colour}" d="{ICONS[slug]}"/></g>'
                f'<text x="{x + 36}" y="{y + 21.5}" font-size="13" font-weight="600" fill="$text">{esc(label)}</text></g></g>')
            x += w + 8
            k += 1
    css = SHARED_CSS + """
.bob{animation:bob 3.2s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
.wave{fill:none;stroke:url(#wv);stroke-width:1.5;opacity:0;animation:wave 7s ease-in-out infinite}
@keyframes wave{0%{opacity:0}5%{opacity:1}14%{opacity:0}100%{opacity:0}}
.ipop{transform-box:fill-box;transform-origin:center;animation:ipop 7s ease-in-out infinite}
@keyframes ipop{0%,12%,100%{transform:scale(1) rotate(0)}5%{transform:scale(1.3) rotate(-10deg)}}
"""
    defs = ('<linearGradient id="wv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$g1"/>'
            '<stop offset="1" stop-color="$g2"/></linearGradient>')
    label = "Tech stack. " + " ".join(f"{g}: {', '.join(i[0] for i in items)}." for g, items in STACK)
    return doc(W, H, label, css, defs, "\n".join(body), t)


# ── open source merge graph ────────────────────────────────────────────────
def opensource(t):
    W, H = 840, 178
    GX, STEP = 268, 58
    body = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="$surface" stroke="$border"/>']
    for r, (repo, sub, key, prs) in enumerate(OSS):
        y = 58 + r * 74
        col = f"${key}"
        end = GX + (len(prs) - 1) * STEP
        body.append(f'<text class="mono" x="24" y="{y - 1}" font-size="12" font-weight="600" fill="$text">{esc(repo)}</text>')
        body.append(f'<text x="24" y="{y + 15}" font-size="11" fill="$muted">{esc(sub)}</text>')
        # the main branch, then a travelling pulse on top of it
        main = f"M{GX - 34} {y}H{W - 28}"
        body.append(f'<path class="main" style="animation-delay:{r * .25:.2f}s" pathLength="1" d="{main}"/>')
        body.append(f'<path class="pulse" style="animation-delay:{2.6 + r * 1.2:.1f}s" pathLength="1" d="{main}"/>')
        span = (W - 28) - (GX - 34)
        for i, pr in enumerate(prs):
            x = GX + i * STEP
            delay = 0.5 + r * 0.25 + i * 0.13
            hump = f"M{x - 28} {y}C{x - 20} {y} {x - 22} {y - 16} {x - 14} {y - 16}C{x - 6} {y - 16} {x - 8} {y} {x} {y}"
            body.append(f'<path class="br" style="animation-delay:{delay:.2f}s" stroke="{col}" pathLength="1" d="{hump}"/>')
            # a commit rides each branch back into main, one after another
            body.append(f'<path class="cd" style="animation-delay:{2 + r * .4 + i * .35:.2f}s" stroke="{col}" '
                        f'pathLength="1" d="{hump}"/>')
            body.append(f'<circle class="pop" style="animation-delay:{delay + .25:.2f}s" cx="{x - 14}" cy="{y - 16}" r="2.6" '
                        f'fill="$surface" stroke="{col}" stroke-width="1.4"/>')
            # ring fires when the travelling pulse reaches this node (the pulse covers the line in 38% of 6s)
            hit = 2.6 + r * 1.2 + (x - (GX - 34)) / span * 6 * .38
            body.append(f'<circle class="ring" stroke="$merged" style="animation:hit 6s ease-out {hit:.2f}s infinite" '
                        f'cx="{x}" cy="{y}" r="4.6"/>')
            body.append(f'<circle class="pop" style="animation-delay:{delay + .4:.2f}s" cx="{x}" cy="{y}" r="4.6" fill="$merged"/>')
            body.append(f'<text class="mono fade" style="animation-delay:{delay + .5:.2f}s" x="{x}" y="{y + 20}" '
                        f'font-size="9.5" fill="$muted" text-anchor="middle">#{pr}</text>')
        if end + 40 < W - 28:
            body.append(f'<text class="mono fade" style="animation-delay:1.6s" x="{W - 28}" y="{y + 20}" font-size="9.5" '
                        f'fill="$muted" text-anchor="end">main</text>')
    css = SHARED_CSS + """
.main{fill:none;stroke:$edge;stroke-opacity:.7;stroke-width:1.6;stroke-linecap:round;stroke-dasharray:1;animation:draw 1.2s ease-out both}
.br{fill:none;stroke-width:1.6;stroke-linecap:round;stroke-dasharray:1;animation:draw .5s ease-out both}
@keyframes draw{from{stroke-dashoffset:1}}
.pulse{fill:none;stroke:$merged;stroke-width:4;stroke-linecap:round;stroke-dasharray:.03 2;opacity:0;animation:run 6s linear infinite}
@keyframes run{0%{stroke-dashoffset:2.03;opacity:0}3%{opacity:1}35%{opacity:1}38%{stroke-dashoffset:1.03;opacity:0}100%{stroke-dashoffset:1.03;opacity:0}}
.cd{fill:none;stroke-width:3.6;stroke-linecap:round;stroke-dasharray:.001 2;opacity:0;animation:cd 4.9s ease-in-out infinite}
@keyframes cd{0%{stroke-dashoffset:2.001;opacity:0}3%{opacity:1}17%{opacity:1}20%{stroke-dashoffset:1.001;opacity:0}100%{stroke-dashoffset:1.001;opacity:0}}
"""
    label = "Merged pull requests. " + " ".join(
        f"{repo}: {len(prs)} merged ({', '.join('#' + str(p) for p in prs)})." for repo, _, _, prs in OSS)
    return doc(W, H, label, css, "", "\n".join(body), t)


# ── arcade ─────────────────────────────────────────────────────────────────
def arcade(t):
    """An auto-playing shooter loop: the ship sweeps a formation of bugs row by row, the
    score climbs, STAGE CLEAR, repeat. Every event is placed on one T-second timeline."""
    W, H, T = 840, 272, 12.0
    XS, YS = [195 + c * 50 for c in range(10)], (84, 116, 148)
    GUN, SHIP_Y, GROUND, SPEED = 214, 228, 250, 620
    BUGS = [("$a3", 30), ("$a2", 20), ("$a4", 10)]  # per row, top first: colour, points
    order = ([(c, 2) for c in range(10)] + [(c, 1) for c in reversed(range(10))] + [(c, 0) for c in range(10)])
    shots = []  # (column, row, fire time, hit time)
    for i, (c, r) in enumerate(order):
        fire = 1.3 + i * .27
        shots.append((c, r, fire, fire + (GUN - YS[r] - 8) / SPEED))

    # the ship stops under each target just long enough to fire
    path = [(0, 420), (.7, 420)]
    for c, r, fire, hit in shots:
        path += [(fire - .05, XS[c]), (fire + .03, XS[c])]
    path += [(10.0, 420), (T, 420)]

    def ship_x(s):
        for (s0, x0), (s1, x1) in zip(path, path[1:]):
            if s0 <= s <= s1:
                return x0 + (x1 - x0) * (s - s0) / (s1 - s0)
        return 420

    kfs = [kf("ship", T, [(s, f"transform:translateX({n(x - 420)}px)") for s, x in path])]
    for j in range(6):  # explosion debris, one direction per particle
        a = math.radians(j * 60 + 30)
        kfs.append(f"@keyframes p{j}{{0%{{transform:translate(0,0);opacity:1}}"
                   f"5%{{transform:translate({n(19 * math.cos(a))}px,{n(19 * math.sin(a))}px);opacity:0}}100%{{opacity:0}}}}")
    for r in range(3):  # a bullet per row distance
        dist, tt = GUN - YS[r] - 8, (GUN - YS[r] - 8) / SPEED
        kfs.append(kf(f"b{r}", T, [(0, "opacity:1;transform:translateY(0)"),
                                   (tt, f"opacity:1;transform:translateY(-{dist}px)"),
                                   (tt + .01, f"opacity:0;transform:translateY(-{dist}px)"),
                                   (T, f"opacity:0;transform:translateY(-{dist}px)")]))

    formation, shots_svg = [], []
    for i, (c, r, fire, hit) in enumerate(shots):
        col, pts = BUGS[r]
        born = .2 + r * .15 + c * .035
        kfs.append(kf(f"k{i}", T, [(0, "opacity:0;transform:scale(0)"), (born, "opacity:0;transform:scale(0)"),
                                   (born + .2, "opacity:1;transform:scale(1.25)"), (born + .32, "transform:scale(1)"),
                                   (hit, "opacity:1;transform:scale(1)"), (hit + .14, "opacity:0;transform:scale(1.8)"),
                                   (T, "opacity:0;transform:scale(1.8)")]))
        d = f"animation-delay:{hit - T:.2f}s"  # phase 0 of the shared effects lands on the hit
        debris = "".join(f'<rect class="p{j}" style="{d}" x="-1.5" y="-1.5" width="3" height="3" rx=".6" fill="{col}"/>'
                         for j in range(6))
        formation.append(
            f'<g transform="translate({XS[c]} {YS[r]})"><g class="bug" style="animation-name:k{i}"><use href="#bug{r}"/></g>'
            f'<circle class="hr" style="{d}" r="6" stroke="{col}"/>{debris}'
            f'<text class="pt mono" style="{d}" y="-14" font-size="10" font-weight="700" fill="$text" '
            f'text-anchor="middle">+{pts}</text></g>')
        f = f"animation-delay:{fire - T:.2f}s"
        shots_svg.append(
            f'<circle class="mf" style="{f}" cx="{XS[c]}" cy="{GUN}" r="4" fill="$g2"/>'
            f'<g transform="translate({XS[c]} {GUN})"><g class="bl" style="animation-name:b{r};{f}">'
            f'<rect x="-3.5" y="-9" width="7" height="16" rx="3.5" fill="$g2" fill-opacity=".25"/>'
            f'<rect x="-1.25" y="-7" width="2.5" height="12" rx="1.25" fill="$g2"/></g></g>')

    # the bugs shoot back now and then, always landing clear of the ship
    drops = []
    for k, s in enumerate((2.2, 4.1, 5.9, 7.6)):
        lowest = {}
        for c, r, _, hit in shots:
            if hit > s + .1:
                lowest[c] = max(lowest.get(c, -1), r)

        def land(c):
            return s + (GROUND - YS[lowest[c]] - 12) / 160

        c = min((c for c in lowest if abs(ship_x(land(c)) - XS[c]) >= 90),
                key=lambda c: abs(abs(ship_x(land(c)) - XS[c]) - 150))
        y0, dist = YS[lowest[c]] + 10, GROUND - YS[lowest[c]] - 22
        kfs.append(kf(f"d{k}", T, [(0, "opacity:0;transform:translateY(0)"), (s, "opacity:0;transform:translateY(0)"),
                                   (s + .01, "opacity:1;transform:translateY(0)"),
                                   (land(c), f"opacity:1;transform:translateY({dist}px)"),
                                   (land(c) + .01, f"opacity:0;transform:translateY({dist}px)"),
                                   (T, f"opacity:0;transform:translateY({dist}px)")]))
        drops.append(f'<g transform="translate({XS[c]} {y0})"><path class="dr" style="animation-name:d{k}" '
                     f'd="M0 0l2.5 3.5-2.5 3.5 2.5 3.5" fill="none" stroke="$err" stroke-width="1.8" '
                     f'stroke-linecap="round" stroke-linejoin="round"/></g>'
                     f'<circle class="hr" style="animation-delay:{land(c) - T:.2f}s" cx="{XS[c]}" cy="{GROUND - 2}" r="4" stroke="$err"/>')

    # score: one label per value, each shown until the next hit
    total, values = 0, [(0, 0)]
    for c, r, _, hit in shots:
        total += BUGS[r][1]
        values.append((hit, total))
    score = []
    for k, (s, v) in enumerate(values):
        if k == 0:
            stops = [(0, "opacity:1"), (values[1][0], "opacity:0"), (T, "opacity:0")]
        elif k == len(values) - 1:
            stops = [(0, "opacity:0"), (s, "opacity:1"), (T, "opacity:1")]
        else:
            stops = [(0, "opacity:0"), (s, "opacity:1"), (values[k + 1][0], "opacity:0"), (T, "opacity:0")]
        kfs.append(kf(f"s{k}", T, stops))
        score.append(f'<text class="sc mono" style="{"opacity:1;" if k == 0 else ""}animation-name:s{k}" x="416" y="31" '
                     f'font-size="14" font-weight="700" fill="$text">{v:06d}</text>')

    kfs.append(kf("rd", T, [(0, "opacity:1"), (.35, "opacity:0"), (.55, "opacity:1"), (.9, "opacity:0"),
                            (1.05, "opacity:1"), (1.25, "opacity:0"), (T, "opacity:0")]))
    kfs.append(kf("clr", T, [(0, "opacity:0;transform:scale(.6)"), (9.6, "opacity:0;transform:scale(.6)"),
                             (9.85, "opacity:1;transform:scale(1.08)"), (10.05, "transform:scale(1)"),
                             (11.4, "opacity:1;transform:scale(1)"), (11.7, "opacity:0;transform:scale(1)"),
                             (T, "opacity:0;transform:scale(1)")]))
    rnd = random.Random(3)
    confetti = []
    for k in range(16):
        a = k / 16 * 2 * math.pi + rnd.uniform(-.2, .2)
        dist = rnd.uniform(70, 140)
        dx, dy = dist * math.cos(a) * 1.7, dist * math.sin(a) * .6
        spin = rnd.choice((1, -1)) * rnd.randint(180, 400)
        kfs.append(kf(f"f{k}", T, [(0, "opacity:0;transform:translate(0,0) rotate(0)"),
                                   (9.62, "opacity:0;transform:translate(0,0) rotate(0)"),
                                   (9.64, "opacity:1;transform:translate(0,0) rotate(0)"),
                                   (10.5, f"opacity:1;transform:translate({n(dx)}px,{n(dy)}px) rotate({spin // 2}deg)"),
                                   (11.4, f"opacity:0;transform:translate({n(dx)}px,{n(dy + 30)}px) rotate({spin}deg)"),
                                   (T, f"opacity:0;transform:translate({n(dx)}px,{n(dy + 30)}px) rotate({spin}deg)")]))
        confetti.append(f'<rect class="cf" style="animation-name:f{k}" x="417" y="116.5" width="6" height="3" rx="1" '
                        f'fill="{("$a1", "$a2", "$a3", "$a4")[k % 4]}"/>')

    def stars(seed, size, count, radii):
        r = random.Random(seed)
        return "".join(f'<circle cx="{r.randint(2, size - 2)}" cy="{r.randint(2, size - 2)}" r="{r.choice(radii)}"/>'
                       for _ in range(count))

    bug_art = []
    for r, (col, _) in enumerate(BUGS):
        legs = f'fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round"'
        bug_art.append(
            f'<g id="bug{r}"><g class="la" {legs}><path d="M-5-3l-6-4M-6 1h-6M-5 5l-6 4M5-3l6-4M6 1h6M5 5l6 4"/></g>'
            f'<g class="lb" {legs}><path d="M-5-3l-6-1M-6 1l-6 3M-5 5l-5 6M5-3l6-1M6 1l6 3M5 5l5 6"/></g>'
            f'<path d="M-2-11l-3-5M2-11l3-5" {legs}/><circle cy="-9" r="4" fill="{col}"/>'
            f'<ellipse cy="2" rx="6.5" ry="7.5" fill="{col}"/><path d="M0-4v13" stroke="$card2" stroke-opacity=".55" '
            f'stroke-width="1.2"/><circle cx="-1.7" cy="-9.6" r="1.1" fill="$node"/><circle cx="1.7" cy="-9.6" r="1.1" '
            f'fill="$node"/></g>')

    css = SHARED_CSS + f"""
.d1{{animation:drift 14s ease-in-out infinite}}
.d2{{animation:drift 17s ease-in-out infinite reverse}}
@keyframes drift{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-26px,16px)}}}}
.sfa{{animation:sfa 10s linear infinite}}
@keyframes sfa{{to{{transform:translateY(140px)}}}}
.sfb{{animation:sfb 6s linear infinite}}
@keyframes sfb{{to{{transform:translateY(100px)}}}}
.la{{animation:la .5s step-end infinite}}
.lb{{animation:la .5s step-end -.25s infinite}}
@keyframes la{{0%{{opacity:1}}50%{{opacity:0}}}}
.fm{{animation:fm 2.6s ease-in-out infinite}}
@keyframes fm{{50%{{transform:translateY(3px)}}}}
.bug{{transform-box:fill-box;transform-origin:center;animation-duration:{n(T)}s;animation-timing-function:linear;animation-iteration-count:infinite}}
.hr{{fill:none;stroke-width:1.6;opacity:0;transform-box:fill-box;transform-origin:center;animation:hr {n(T)}s ease-out infinite}}
@keyframes hr{{0%{{transform:scale(.6);opacity:1}}5%{{transform:scale(3.2);opacity:0}}100%{{transform:scale(3.2);opacity:0}}}}
.p0,.p1,.p2,.p3,.p4,.p5{{opacity:0;animation-duration:{n(T)}s;animation-timing-function:cubic-bezier(.2,.7,.4,1);animation-iteration-count:infinite}}
.p0{{animation-name:p0}}.p1{{animation-name:p1}}.p2{{animation-name:p2}}.p3{{animation-name:p3}}.p4{{animation-name:p4}}.p5{{animation-name:p5}}
.pt{{opacity:0;animation:pt {n(T)}s ease-out infinite}}
@keyframes pt{{0%{{opacity:1;transform:translateY(0)}}7%{{opacity:0;transform:translateY(-18px)}}100%{{opacity:0;transform:translateY(-18px)}}}}
.bl,.dr,.cf{{opacity:0;animation-duration:{n(T)}s;animation-timing-function:linear;animation-iteration-count:infinite}}
.cf{{transform-box:fill-box;transform-origin:center;animation-timing-function:ease-out}}
.mf{{opacity:0;transform-box:fill-box;transform-origin:center;animation:mf {n(T)}s ease-out infinite}}
@keyframes mf{{0%{{opacity:.9;transform:scale(1)}}1.5%{{opacity:0;transform:scale(2.4)}}100%{{opacity:0;transform:scale(2.4)}}}}
.ship{{animation:ship {n(T)}s ease-in-out infinite}}
.hov{{animation:hov 1.6s ease-in-out infinite}}
@keyframes hov{{50%{{transform:translateY(-2px)}}}}
.fl{{transform-box:fill-box;transform-origin:50% 0;animation:fl .14s ease-in-out infinite alternate}}
@keyframes fl{{to{{transform:scaleY(.55)}}}}
.sc{{opacity:0;animation-duration:{n(T)}s;animation-timing-function:step-end;animation-iteration-count:infinite}}
.rd{{animation:rd {n(T)}s step-end infinite}}
.clr{{opacity:0;transform-box:fill-box;transform-origin:center;animation:clr {n(T)}s ease-out infinite}}
""" + "\n".join(kfs)

    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$card1"/><stop offset="1" stop-color="$card2"/></linearGradient>
<radialGradient id="ga"><stop offset="0" stop-color="$a3" stop-opacity="$glowop"/><stop offset="1" stop-color="$a3" stop-opacity="0"/></radialGradient>
<radialGradient id="gb"><stop offset="0" stop-color="$g2" stop-opacity="$glowop"/><stop offset="1" stop-color="$g2" stop-opacity="0"/></radialGradient>
<radialGradient id="sg"><stop offset="0" stop-color="$g2" stop-opacity=".45"/><stop offset="1" stop-color="$g2" stop-opacity="0"/></radialGradient>
<linearGradient id="gl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="$g1" stop-opacity="0"/><stop offset=".5" stop-color="$g2"/><stop offset="1" stop-color="$g1" stop-opacity="0"/></linearGradient>
{HUB}
<pattern id="s1" width="140" height="140" patternUnits="userSpaceOnUse"><g fill="$muted">{stars(11, 140, 9, (.7, .9, 1.2))}</g></pattern>
<pattern id="s2" width="100" height="100" patternUnits="userSpaceOnUse"><g fill="$edge">{stars(12, 100, 5, (.5, .7))}</g></pattern>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
{SHIP}
{"".join(bug_art)}
"""
    lives = "".join(f'<use href="#ship" transform="translate({x} 26) scale(.5)"/>' for x in (758, 778, 798))
    body = f"""
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<g clip-path="url(#card)">
<circle class="d1" cx="760" cy="40" r="260" fill="url(#ga)"/>
<circle class="d2" cx="80" cy="300" r="240" fill="url(#gb)"/>
<rect class="sfa" y="-140" width="{W}" height="{H + 140}" fill="url(#s1)" opacity=".6"/>
<rect class="sfb" y="-100" width="{W}" height="{H + 100}" fill="url(#s2)" opacity=".5"/>
<rect x="0" y="{GROUND}" width="{W}" height="1.5" fill="url(#gl)"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="$border"/>
<rect class="beam" stroke="url(#hub)" pathLength="100" x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="17.25"/>
<text class="mono blink" x="24" y="31" font-size="12" font-weight="700" fill="$a4">1UP</text>
<text class="mono" x="56" y="31" font-size="12" font-weight="700" fill="$text">ASHWIN</text>
<text class="mono" x="408" y="31" font-size="11" fill="$muted" text-anchor="end">SCORE</text>
{"".join(score)}
<text class="mono" x="740" y="31" font-size="11" fill="$muted" text-anchor="end">LIVES</text>
{lives}
<path d="M18 44H822" stroke="$border" stroke-dasharray="2 4"/>
<g class="fm">{"".join(formation)}</g>
{"".join(drops)}
{"".join(shots_svg)}
<g class="ship"><g transform="translate(420 {SHIP_Y})"><g class="hov">
<ellipse cy="15" rx="22" ry="6" fill="url(#sg)"/>
<path class="fl" d="M-3.5 7L0 18 3.5 7Z" fill="$a4"/><path class="fl" style="animation-delay:-.07s" d="M-1.8 7L0 13 1.8 7Z" fill="#fff" fill-opacity=".85"/>
<use href="#ship"/></g></g></g>
<text class="rd mono" x="420" y="196" font-size="13" font-weight="700" fill="$a1" text-anchor="middle" letter-spacing="2">PLAYER 1 · READY</text>
<g class="clr"><text class="mono" x="420" y="126" font-size="30" font-weight="800" fill="url(#hub)" text-anchor="middle" letter-spacing="4">STAGE CLEAR</text>
<text class="mono" x="420" y="152" font-size="12" fill="$muted" text-anchor="middle">30 bugs squashed · ready to ship</text></g>
{"".join(confetti)}
<text class="mono blink" x="24" y="265" font-size="10.5" font-weight="700" fill="$a1">● AUTO-PLAY</text>
<text class="mono" x="420" y="265" font-size="10.5" fill="$muted" text-anchor="middle">squash bugs · merge PRs · ship features</text>
<text class="mono" x="816" y="265" font-size="10.5" fill="$muted" text-anchor="end">CREDIT 01</text>
"""
    label = ("Animated arcade loop: a ship clears a formation of 30 bugs row by row while the score climbs to "
             f"{total}, then STAGE CLEAR.")
    return doc(W, H, label, css, defs, body, t)


# ── section headings ───────────────────────────────────────────────────────
def section(t, idx, title, tag):
    W, H, ADV, X, Y, DT, T0 = 840, 66, 13.2, 46, 46, .04, .2
    tw = len(title) * ADV
    typed = T0 + len(title) * DT
    chars, clip = [], []
    for i, ch in enumerate(title):
        if ch == " ":
            continue
        x = n(X + i * ADV)
        chars.append(f'<text class="fade" style="animation-duration:.3s;animation-delay:{T0 + i * DT:.2f}s" '
                     f'x="{x}" y="{Y}">{esc(ch)}</text>')
        clip.append(f'<text class="mono" x="{x}" y="{Y}" font-size="22" font-weight="700">{esc(ch)}</text>')
    tag_w = len(tag) * 6.9
    dot = n(W - 2 - tag_w - 11)
    line = f"M{X} {Y + 11}H{n(X + tw)}"
    css = SHARED_CSS + f"""
.g{{animation:run 7s cubic-bezier(.45,0,.55,1) infinite}}
@keyframes run{{from{{transform:translateX(-160px)}}to{{transform:translateX(840px)}}}}
.fly{{animation:fly 11s cubic-bezier(.4,0,.6,1) infinite}}
@keyframes fly{{0%{{transform:translateX(0)}}26%,100%{{transform:translateX(1000px)}}}}
.cur{{animation:cur {n(typed - T0)}s steps({len(title)},start) {T0}s both}}
@keyframes cur{{from{{transform:translateX(-{n(tw)}px)}}}}
.ul{{fill:none;stroke-width:2.2;stroke-linecap:round;stroke-dasharray:1;animation:draw .9s cubic-bezier(.22,1,.36,1) {typed:.2f}s both}}
@keyframes draw{{from{{stroke-dashoffset:1}}}}
.pk{{fill:none;stroke:$g2;stroke-width:5;stroke-linecap:round;stroke-dasharray:.001 2;opacity:0;animation:flow 5s ease-in-out {typed + 1.2:.2f}s infinite}}
@keyframes flow{{0%{{stroke-dashoffset:2.001;opacity:0}}6%{{opacity:1}}40%{{opacity:1}}46%{{stroke-dashoffset:1.001;opacity:0}}100%{{stroke-dashoffset:1.001;opacity:0}}}}
.sheen{{opacity:0;animation:sheen 8s ease-in-out {typed + .4 + idx * .5:.2f}s infinite}}
@keyframes sheen{{0%{{transform:translateX(0);opacity:0}}5%{{opacity:1}}24%{{transform:translateX({n(tw + 180)}px);opacity:1}}28%,100%{{transform:translateX({n(tw + 180)}px);opacity:0}}}}
"""
    defs = f"""
<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="$border" stop-opacity="0"/><stop offset=".5" stop-color="$border"/><stop offset="1" stop-color="$border" stop-opacity="0"/></linearGradient>
<linearGradient id="gl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="$g1" stop-opacity="0"/><stop offset=".5" stop-color="$g2"/><stop offset="1" stop-color="$g1" stop-opacity="0"/></linearGradient>
<linearGradient id="tr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="$g2" stop-opacity="0"/><stop offset="1" stop-color="$g2" stop-opacity=".8"/></linearGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="$g1" stop-opacity="0"/><stop offset=".5" stop-color="$g2"/><stop offset="1" stop-color="$g1" stop-opacity="0"/></linearGradient>
<linearGradient id="ug" gradientUnits="userSpaceOnUse" x1="{X}" y1="0" x2="{n(X + tw)}" y2="0"><stop offset="0" stop-color="$g1"/><stop offset="1" stop-color="$g2"/></linearGradient>
{HUB}
{SHIP}
<clipPath id="tc">{"".join(clip)}</clipPath>
"""
    body = f"""
<rect y="7.5" width="{W}" height="1" fill="url(#ln)"/>
<rect class="g" style="animation-delay:{-idx * 1.1:.1f}s" y="7" width="160" height="2" rx="1" fill="url(#gl)"/>
<g class="fly" style="animation-delay:{1.2 + idx * 1.7:.1f}s"><rect x="-112" y="6.8" width="64" height="2.4" rx="1.2" fill="url(#tr)"/><g transform="translate(-40 8) rotate(90) scale(.6)"><use href="#ship"/></g></g>
<text class="mono fade" x="2" y="{Y}" font-size="13" font-weight="700" fill="$a1">{idx:02d}<tspan fill="$faint"> /</tspan></text>
<g class="mono" font-size="22" font-weight="700" fill="$text">{"".join(chars)}</g>
<g clip-path="url(#tc)"><g transform="skewX(-18)"><rect class="sheen" x="{X - 75}" y="{Y - 24}" width="60" height="32" fill="url(#sh)"/></g></g>
<g class="cur"><rect class="blink" x="{n(X + tw + 4)}" y="{Y - 18}" width="11" height="22" rx="2" fill="$a1"/></g>
<path class="ul" pathLength="1" stroke="url(#ug)" d="{line}"/>
<path class="pk" pathLength="1" d="{line}"/>
<g class="fade" style="animation-delay:{typed:.2f}s"><circle class="ring" stroke="$a1" cx="{dot}" cy="{Y - 4.5}" r="3"/><circle cx="{dot}" cy="{Y - 4.5}" r="3" fill="$a1"/>
<text class="mono" x="{W - 2}" y="{Y}" font-size="11.5" fill="$muted" text-anchor="end" textLength="{n(tag_w)}" lengthAdjust="spacingAndGlyphs">{esc(tag)}</text></g>
"""
    return doc(W, H, f"{title} — {tag}", css, defs, body, t)


# ── project covers ─────────────────────────────────────────────────────────
def motif_bars(col):
    heights = [24, 38, 30, 50, 62]
    out = ['<path d="M270 88H376" stroke="$faint" stroke-width="1.2" stroke-linecap="round"/>',
           f'<path d="M270 34H376" stroke="{col}" stroke-opacity=".5" stroke-dasharray="3 4"/>']
    for i, h in enumerate(heights):
        out.append(f'<rect class="bar" style="animation-delay:{-i * .45:.2f}s" x="{276 + i * 20}" y="{88 - h}" width="13" '
                   f'height="{h}" rx="3" fill="{col}" fill-opacity="{.45 + i * .13:.2f}"/>')
    css = """
.bar{transform-box:fill-box;transform-origin:bottom;animation:bar 3.6s ease-in-out infinite}
@keyframes bar{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.6)}}
"""
    return "".join(out), css


def motif_pods(col):
    out = [f'<path class="load" pathLength="1" d="M276 40C292 40 296 24 312 26S334 36 346 28S366 18 376 20" '
           f'fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round"/>']
    k = 0
    for c in range(6):
        for r in (2, 1, 0):  # fill each column bottom-up, like replicas being added
            out.append(f'<rect class="pod" style="animation-delay:{k * .16 - 6:.2f}s" x="{276 + c * 17}" y="{50 + r * 15}" '
                       f'width="12" height="11" rx="3" fill="{col}"/>')
            k += 1
    css = """
.pod{animation:pod 6s ease-in-out infinite}
@keyframes pod{0%{opacity:.16}6%{opacity:1}52%{opacity:1}60%{opacity:.16}100%{opacity:.16}}
.load{stroke-dasharray:1;animation:load 6s ease-in-out infinite}
@keyframes load{0%{stroke-dashoffset:1}45%{stroke-dashoffset:0}85%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
"""
    return "".join(out), css


def motif_chat(col):
    out = [
        f'<g class="bub" style="transform-origin:262px 40px"><rect x="262" y="22" width="78" height="20" rx="10" '
        f'fill="$chip" stroke="$border"/><rect x="273" y="30.5" width="44" height="3" rx="1.5" fill="$muted" fill-opacity=".7"/></g>',
        f'<g class="bub" style="transform-origin:378px 66px;animation-delay:.9s"><rect x="296" y="48" width="82" height="20" '
        f'rx="10" fill="{col}" fill-opacity=".9"/><rect x="307" y="56.5" width="52" height="3" rx="1.5" fill="$node" fill-opacity=".8"/></g>',
        f'<g class="bub" style="transform-origin:262px 92px;animation-delay:1.8s"><rect x="262" y="74" width="50" height="20" '
        f'rx="10" fill="$chip" stroke="{col}"/>'
        + "".join(f'<circle class="dot" style="animation-delay:{i * .18:.2f}s" cx="{277 + i * 10}" cy="84" r="2.3" fill="{col}"/>'
                  for i in range(3)) + "</g>",
    ]
    css = """
.bub{animation:bub 6s cubic-bezier(.34,1.4,.64,1) infinite}
@keyframes bub{0%{transform:scale(0);opacity:0}7%{transform:scale(1);opacity:1}82%{transform:scale(1);opacity:1}90%,100%{transform:scale(1);opacity:0}}
.dot{transform-box:fill-box;animation:dot 1.1s ease-in-out infinite}
@keyframes dot{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-3.5px)}}
"""
    return "".join(out), css


def motif_notes(col):
    lines = [(304, 40, 44), (304, 51, 36), (304, 62, 44), (304, 73, 26)]
    out = [f'<rect x="300" y="20" width="66" height="76" rx="7" fill="{col}" fill-opacity=".22" transform="rotate(8 333 58)"/>',
           '<rect x="292" y="18" width="66" height="76" rx="7" fill="$chip" stroke="$border"/>',
           f'<rect x="304" y="27" width="22" height="4" rx="2" fill="{col}"/>']
    for i, (x, y, w) in enumerate(lines):
        out.append(f'<path class="ln" style="animation-delay:{i * .35:.2f}s" pathLength="1" d="M{x} {y}h{w}" '
                   f'stroke="$muted" stroke-width="2.4" stroke-linecap="round"/>')
    out.append(f'<g class="chk" style="transform-origin:358px 94px"><circle cx="358" cy="94" r="10" fill="{col}"/>'
               '<path d="M353.5 94.2l3.2 3.2 5.8-6.4" fill="none" stroke="$node" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round"/></g>')
    css = """
.ln{stroke-dasharray:1;animation:ln 6s ease-out infinite}
@keyframes ln{0%{stroke-dashoffset:1;opacity:1}12%{stroke-dashoffset:0}84%{stroke-dashoffset:0;opacity:1}92%,100%{stroke-dashoffset:0;opacity:0}}
.chk{animation:chk 6s cubic-bezier(.34,1.56,.64,1) infinite}
@keyframes chk{0%,28%{transform:scale(0);opacity:0}36%{transform:scale(1);opacity:1}84%{transform:scale(1);opacity:1}92%,100%{transform:scale(1);opacity:0}}
"""
    return "".join(out), css


MOTIFS = {"bars": motif_bars, "pods": motif_pods, "chat": motif_chat, "notes": motif_notes}


def cover(t, slug):
    W, H = 396, 116
    name, tag, key, motif = COVERS[slug]
    col = f"${key}"
    art, art_css = MOTIFS[motif](col)
    rnd = random.Random(slug)
    motes = "".join(f'<circle class="mote" style="animation-delay:{-rnd.uniform(0, 6):.1f}s" cx="{rnd.randint(190, 384)}" '
                    f'cy="{H + 4}" r="{rnd.choice((1, 1.4, 1.8))}" fill="{col}"/>' for _ in range(8))
    css = SHARED_CSS + art_css + """
.gl{animation:gl 10s ease-in-out infinite}
@keyframes gl{0%,100%{transform:translate(0,0)}50%{transform:translate(-18px,8px)}}
.mote{opacity:0;animation:mote 6s linear infinite}
@keyframes mote{0%{transform:translateY(0);opacity:0}20%{opacity:.7}100%{transform:translateY(-110px);opacity:0}}
"""
    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$card1"/><stop offset="1" stop-color="$card2"/></linearGradient>
<radialGradient id="ga"><stop offset="0" stop-color="{col}" stop-opacity="$glowop"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="12"/></clipPath>
"""
    body = f"""
<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>
<g clip-path="url(#card)"><circle class="gl" cx="340" cy="50" r="150" fill="url(#ga)"/>{motes}{art}</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="11.5" fill="none" stroke="$border"/>
<rect class="beam" stroke="{col}" pathLength="100" x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="11.25"/>
<rect x="22" y="33" width="26" height="3" rx="1.5" fill="{col}"/>
<text x="22" y="64" font-size="18" font-weight="800" letter-spacing="-.2" fill="$text">{esc(name)}</text>
<text class="mono" x="22" y="85" font-size="9.5" letter-spacing=".9" fill="{col}">{esc(tag)}</text>
"""
    return doc(W, H, f"{name} — {tag.title()}", css, defs, body, t)


# ── footer ─────────────────────────────────────────────────────────────────
def footer(t):
    W, H = 840, 168

    def wave(y, amp, length):
        """A sine-like path one wavelength wider than the card on each side, so it can loop seamlessly."""
        half = length / 2
        d = f"M{-length} {y}Q{n(-length + half / 2)} {y - amp} {n(-length + half)} {y}"
        x = -length + half
        while x < W + length:
            x += half
            d += f"T{n(x)} {y}"
        return d

    rnd = random.Random(9)
    motes = "".join(f'<circle class="mote" style="animation-delay:{-rnd.uniform(0, 9):.1f}s;animation-duration:{rnd.uniform(6, 10):.1f}s" '
                    f'cx="{rnd.randint(24, 816)}" cy="{H + 4}" r="{rnd.choice((1.2, 1.6, 2))}" '
                    f'fill="{rnd.choice(("$g1", "$g2", "$a3"))}"/>' for _ in range(20))
    headline = 'x="420" y="66" font-size="30" font-weight="800" letter-spacing="-.4" text-anchor="middle"'
    css = SHARED_CSS + """
.w{fill:none;stroke-width:1.4}
.w1{animation:w1 9s linear infinite}
.w2{animation:w2 13s linear infinite}
.w3{animation:w1 17s linear infinite reverse}
@keyframes w1{to{transform:translateX(240px)}}
@keyframes w2{to{transform:translateX(-180px)}}
.d1{animation:drift 14s ease-in-out infinite}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(30px,-10px)}}
.mote{opacity:0;animation:mote 8s linear infinite}
@keyframes mote{0%{transform:translateY(0);opacity:0}15%{opacity:.8}100%{transform:translateY(-160px);opacity:0}}
.sheen{opacity:0;animation:sheen 6s ease-in-out 1.6s infinite}
@keyframes sheen{0%{transform:translateX(0);opacity:0}6%{opacity:1}30%{transform:translateX(560px);opacity:1}34%,100%{transform:translateX(560px);opacity:0}}
.fly{animation:fly 9s ease-in-out 2.4s infinite}
@keyframes fly{0%{transform:translate(0,0)}9%{transform:translate(240px,-8px)}18%{transform:translate(480px,5px)}27%{transform:translate(720px,-6px)}36%,100%{transform:translate(960px,0)}}
"""
    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$card1"/><stop offset="1" stop-color="$card2"/></linearGradient>
<radialGradient id="ga"><stop offset="0" stop-color="$g1" stop-opacity="$glowop"/><stop offset="1" stop-color="$g1" stop-opacity="0"/></radialGradient>
<linearGradient id="hl" gradientUnits="userSpaceOnUse" x1="455" y1="0" x2="725" y2="0"><stop offset="0" stop-color="$g1"/><stop offset="1" stop-color="$g2"/></linearGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="tr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="$g2" stop-opacity="0"/><stop offset="1" stop-color="$g2" stop-opacity=".8"/></linearGradient>
{HUB}
{SHIP}
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<clipPath id="hc"><text {headline}>Let’s build something production-ready.</text></clipPath>
"""
    body = f"""
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<g clip-path="url(#card)">
<circle class="d1" cx="420" cy="210" r="300" fill="url(#ga)"/>
{motes}
<path class="w w1" stroke="$g1" stroke-opacity=".5" d="{wave(132, 9, 240)}"/>
<path class="w w2" stroke="$g2" stroke-opacity=".4" d="{wave(140, 12, 180)}"/>
<path class="w w3" stroke="$edge" stroke-opacity=".35" d="{wave(148, 7, 240)}"/>
<g class="fly"><rect x="-130" y="116.8" width="80" height="2.4" rx="1.2" fill="url(#tr)"/><g transform="translate(-40 118) rotate(90) scale(.7)"><use href="#ship"/></g></g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="$border"/>
<rect class="beam" stroke="url(#hub)" pathLength="100" x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="17.25"/>
<g class="up"><text {headline} fill="$text">Let’s build something <tspan fill="url(#hl)">production-ready.</tspan></text>
<g clip-path="url(#hc)"><g transform="skewX(-18)"><rect class="sheen" x="140" y="30" width="80" height="46" fill="url(#sh)"/></g></g></g>
<g class="up" style="animation-delay:.15s"><text x="420" y="97" font-size="14" fill="$muted" text-anchor="middle">Open to software engineering internships and full-time roles · 2027 grad</text></g>
"""
    return doc(W, H, "Let's build something production-ready. Open to software engineering internships and "
               "full-time roles, 2027 grad.", css, defs, body, t)


# ── buttons ────────────────────────────────────────────────────────────────
GLYPHS = {
    "globe": '<g fill="none" stroke="{c}" stroke-width="1.4"><circle cx="8" cy="8" r="6.3"/>'
             '<ellipse cx="8" cy="8" rx="2.7" ry="6.3"/><path d="M1.7 8h12.6"/></g>',
    "doc": '<g fill="none" stroke="{c}" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round">'
           '<path d="M4 1.7h5.5L12.3 4.5v9.8H4z"/><path d="M6.3 8h3.6M6.3 10.8h3.6"/></g>',
    "in": '<rect x="1.5" y="1.5" width="13" height="13" rx="3" fill="{c}"/>'
          '<g fill="{bg}"><circle cx="5.2" cy="5.1" r="1.05"/><rect x="4.3" y="6.9" width="1.8" height="4.8"/>'
          '<path d="M7.6 6.9h1.7v.7c.4-.6 1-.9 1.7-.9 1.3 0 1.9.8 1.9 2.2v2.8h-1.8V9.3c0-.6-.2-1-.8-1s-.9.4-.9 1v2.4H7.6z"/></g>',
    "mail": '<g fill="none" stroke="{c}" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round">'
            '<rect x="1.7" y="3.2" width="12.6" height="9.6" rx="1.8"/><path d="M2.2 4.4L8 8.8l5.8-4.4"/></g>',
}


def button(t, label, width, glyph, primary, idx):
    H = 36
    if primary:
        fill, stroke, ink, icon, shine = "url(#p)", "none", "$onaccent", "$onaccent", ".55"
    else:
        fill, stroke, ink, icon, shine = "$surface", "$border", "$text", "$a1", ".2"
    if glyph == "gitlab":
        g = f'<path transform="translate(14 10) scale({16 / 24:.4f})" fill="{icon}" d="{ICONS["gitlab"]}"/>'
    else:
        bg = "$g1" if primary else "$surface"
        g = f'<g transform="translate(14 10)">{GLYPHS[glyph].format(c=icon, bg=bg)}</g>'
    # the shine sweeps along the row of buttons, one after another
    css = f"""
.s{{opacity:0;animation:s 5s ease-in-out {1 + idx * .3:.1f}s infinite}}
@keyframes s{{0%{{transform:translateX(0);opacity:0}}8%{{opacity:1}}34%{{transform:translateX(200px);opacity:1}}38%,100%{{transform:translateX(200px);opacity:0}}}}
"""
    defs = f"""
<linearGradient id="p" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$g1"/><stop offset="1" stop-color="$g2"/></linearGradient>
<linearGradient id="sg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity="{shine}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="b"><rect width="{width}" height="{H}" rx="10"/></clipPath>
"""
    body = f"""
<rect x=".5" y=".5" width="{width - 1}" height="{H - 1}" rx="9.5" fill="{fill}" stroke="{stroke}"/><g clip-path="url(#b)"><g transform="skewX(-20)"><rect class="s" x="-40" width="34" height="36" fill="url(#sg)"/></g></g>
{g}<text x="38" y="22.7" font-size="13" font-weight="600" fill="{ink}">{esc(label)}</text>
"""
    return doc(width, H, label, css, defs, body, t)


def main():
    OUT.mkdir(exist_ok=True)
    files = {}
    for theme, t in THEMES.items():
        files[f"hero-{theme}.svg"] = hero(t)
        files[f"metrics-{theme}.svg"] = metrics(t)
        files[f"arcade-{theme}.svg"] = arcade(t)
        files[f"timeline-{theme}.svg"] = timeline(t)
        files[f"opensource-{theme}.svg"] = opensource(t)
        files[f"stack-{theme}.svg"] = stack(t, theme)
        files[f"footer-{theme}.svg"] = footer(t)
        for idx, (slug, title, tag) in enumerate(SECTIONS, 1):
            files[f"h-{slug}-{theme}.svg"] = section(t, idx, title, tag)
    # Linked images get a single dark version: GitHub rewrites <a><picture>…</picture></a> so the
    # link ends up pointing at the image file, which rules out theme switching for anything clickable.
    dark = THEMES["dark"]
    for slug in COVERS:
        files[f"cover-{slug}.svg"] = cover(dark, slug)
    for idx, (slug, label, width, glyph, primary) in enumerate(BUTTONS):
        files[f"btn-{slug}.svg"] = button(dark, label, width, glyph, primary, idx)
    for name, svg in sorted(files.items()):
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"{len(svg.encode()) / 1024:6.1f} KB  assets/{name}")


if __name__ == "__main__":
    main()
