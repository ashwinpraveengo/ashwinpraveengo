#!/usr/bin/env python3
"""Generate the animated SVGs used by README.md (dark and light copies of the infographics,
one dark copy of the clickable buttons and project covers).

    python3 scripts/build_assets.py

Everything is plain SVG + CSS: no scripts, no external fonts or images, so the
files animate when GitHub serves them through <img>. Edit the data blocks
(PHRASES, METRICS, ROWS, MILESTONES, STACK) and re-run to update the visuals.
Tech icons in icons.json come from Simple Icons (CC0).
"""
import json
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
        ok="#3fb950", merged="#a371f7", node="#0d1117", glowop="0.24", sheenop="0.16", onaccent="#04130d",
    ),
    "light": dict(
        card1="#ffffff", card2="#eef5f6", surface="#f6f8fa", chip="#ffffff", border="#d0d7de",
        text="#1f2328", body="#3b434b", muted="#59636e", faint="#c3ccd5", edge="#8c959f",
        a1="#047857", a2="#0e7490", a3="#6d28d9", a4="#b45309", g1="#10b981", g2="#06b6d4",
        ok="#1a7f37", merged="#8250df", node="#ffffff", glowop="0.20", sheenop="0.45", onaccent="#04130d",
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

# (number, suffix, label, sub-label)
METRICS = [
    ("9.42", "/10", "CGPA", "B.Tech CSE · Amrita"),
    ("1,000+", "", "App downloads", "Priyamvada · Flutter"),
    ("14", "", "PRs merged upstream", "CARE · Scribe-Android"),
    ("2×", "", "Hackathon honors", "Runner-up · Finalist"),
]

NOW = 2026.87  # Nov 2026 — where the "now" marker sits on the timeline
# (title, sub, start, end, colour key, label inside/after the bar, ongoing)
ROWS = [
    ("B.Tech CSE · Amrita", "CGPA 9.42 · 2023 – 2027", 2023.60, 2027.40, "a3", "2023 – 2027", True),
    ("Traboda CyberLabs", "Software Developer Intern", 2024.08, 2025.42, "a2", "Feb 2024 – May 2025", False),
    ("Pupilfirst", "Jr. Full Stack Engineer Intern", 2025.08, 2025.67, "a4", "Feb – Aug 2025", False),
    ("CIR Skill Platform", "Team Lead · Django + GraphQL", 2025.25, NOW, "a1", "Apr 2025 – present", True),
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


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def n(v):
    """Compact number formatting for coordinates."""
    return f"{v:.2f}".rstrip("0").rstrip(".")


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
"""


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
    for i, (x, y, r) in enumerate(nodes):
        delay = f"animation-delay:{0.5 + i * 0.07:.2f}s"
        if i == 0:
            mesh.append(f'<g class="pop" style="{delay}"><circle cx="{x}" cy="{y}" r="{r + 6}" fill="none" '
                        f'stroke="$g1" stroke-opacity=".35"/><circle cx="{x}" cy="{y}" r="{r}" fill="url(#hub)"/>'
                        f'<circle cx="{x}" cy="{y}" r="3" fill="$node"/></g>')
        else:
            stroke = "$g2" if i % 2 else "$g1"
            mesh.append(f'<circle class="pop nd" style="{delay}" stroke="{stroke}" cx="{x}" cy="{y}" r="{r}"/>')

    # typed line
    ADV, X0, Y, DT, SLOT, FADE = 9.0, 70, 182, 0.045, 4.6, 0.3
    T = SLOT * len(PHRASES)
    vis = SLOT - 0.4
    typed, kf = [], []
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
        kf.append(f"@keyframes cur{j}{{0%{{transform:translateX(0);animation-timing-function:steps({len(s)},start)}}"
                  f"{len(s) * DT / T * 100:.3f}%{{transform:translateX({n(width)}px)}}"
                  f"100%{{transform:translateX({n(width)}px)}}}}")
        typed.append(
            f'<g class="ph" style="opacity:{0 if j else 1};animation-delay:{gdelay:.2f}s">{"".join(chars)}'
            f'<g style="animation:cur{j} {n(T)}s linear {gdelay:.2f}s infinite">'
            f'<rect class="blink" x="{X0 + 2}" y="{Y - 13}" width="8" height="16" rx="1.5"/></g></g>')
    a, b = (vis - FADE) / T * 100, vis / T * 100

    css = SHARED_CSS + f"""
.e{{fill:none;stroke:$edge;stroke-opacity:.55;stroke-width:1;stroke-dasharray:1;animation:draw 1.1s ease-out both}}
@keyframes draw{{from{{stroke-dashoffset:1}}}}
.pk{{fill:none;stroke:$g2;stroke-width:3.4;stroke-linecap:round;stroke-dasharray:.001 2;opacity:0;animation:flow 5.5s linear infinite}}
@keyframes flow{{0%{{stroke-dashoffset:2.001;opacity:0}}5%{{opacity:1}}31%{{opacity:1}}36%{{stroke-dashoffset:1.001;opacity:0}}100%{{stroke-dashoffset:1.001;opacity:0}}}}
.nd{{fill:$node;stroke-width:1.5}}
.float{{animation:float 9s ease-in-out infinite}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
.d1{{animation:drift 14s ease-in-out infinite}}
.d2{{animation:drift 17s ease-in-out infinite reverse}}
@keyframes drift{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-26px,16px)}}}}
.sheen{{opacity:0;animation:sheen 7s ease-in-out 1.4s infinite}}
@keyframes sheen{{0%{{transform:translateX(0);opacity:0}}6%{{opacity:1}}26%{{transform:translateX(580px);opacity:1}}30%,100%{{transform:translateX(580px);opacity:0}}}}
.c{{fill:$body;animation:ch {n(T)}s step-end infinite}}
.k{{fill:$a1}}
@keyframes ch{{0%{{opacity:1}}50%{{opacity:0}}100%{{opacity:0}}}}
.ph{{animation:ph {n(T)}s linear infinite}}
@keyframes ph{{0%{{opacity:1}}{a:.3f}%{{opacity:1}}{b:.3f}%{{opacity:0}}100%{{opacity:0}}}}
.blink{{fill:$a1;animation:blink 1.1s step-end infinite}}
@keyframes blink{{0%{{opacity:1}}55%{{opacity:0}}100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.blink{{display:none}}}}
""" + "\n".join(kf)

    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$card1"/><stop offset="1" stop-color="$card2"/></linearGradient>
<radialGradient id="ga"><stop offset="0" stop-color="$g1" stop-opacity="$glowop"/><stop offset="1" stop-color="$g1" stop-opacity="0"/></radialGradient>
<radialGradient id="gb"><stop offset="0" stop-color="$g2" stop-opacity="$glowop"/><stop offset="1" stop-color="$g2" stop-opacity="0"/></radialGradient>
<linearGradient id="hub" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$g1"/><stop offset="1" stop-color="$g2"/></linearGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="$g1" stop-opacity="0"/><stop offset=".5" stop-color="$g2"/><stop offset="1" stop-color="$g1" stop-opacity="0"/></linearGradient>
<linearGradient id="fd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".45" stop-color="#fff"/></linearGradient>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="$faint"/></pattern>
<mask id="dm"><rect x="400" width="440" height="{H}" fill="url(#fd)"/></mask>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<clipPath id="nm"><text x="46" y="138" font-size="44" font-weight="800" letter-spacing="-.6">{esc(NAME)}</text></clipPath>
"""
    body = f"""
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<g clip-path="url(#card)">
<circle class="d1" cx="720" cy="20" r="270" fill="url(#ga)"/>
<circle class="d2" cx="90" cy="330" r="250" fill="url(#gb)"/>
<rect x="400" width="440" height="{H}" fill="url(#dots)" mask="url(#dm)" opacity=".7"/>
<g class="float">{"".join(mesh)}</g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="$border"/>
<g class="up" style="animation-delay:.05s"><text class="mono" x="48" y="84" font-size="13" letter-spacing=".4" fill="$a1">{esc(HANDLE)}<tspan fill="$muted">()</tspan></text></g>
<g class="up" style="animation-delay:.15s"><g clip-path="url(#nm)"><rect x="36" y="94" width="560" height="60" fill="$text"/><g transform="skewX(-18)"><rect class="sheen" x="10" y="88" width="90" height="72" fill="url(#sh)"/></g></g></g>
<g class="up mono" style="animation-delay:.3s" font-size="15"><path d="M49 {Y - 10}l6 5-6 5" fill="none" stroke="$a1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>{"".join(typed)}</g>
<g class="up" style="animation-delay:.45s"><rect x="48" y="212" width="292" height="32" rx="16" fill="$surface" fill-opacity=".75" stroke="$border"/><circle class="ring" stroke="$ok" style="animation-duration:2.4s" cx="67" cy="228" r="4"/><circle cx="67" cy="228" r="4" fill="$ok"/><text x="82" y="232.5" font-size="13" font-weight="600" fill="$text">{esc(STATUS)}</text><text x="356" y="232.5" font-size="12.5" fill="$muted">{esc(LOCATION)}</text></g>
"""
    label = f"{NAME} — software engineer, full-stack and mobile. {STATUS}. {LOCATION}."
    return doc(W, H, label, css, defs, body, t)


# ── metrics ────────────────────────────────────────────────────────────────
def metrics(t):
    W, H, TW, GAP = 840, 124, 198, 16
    BASE, STEP, SIZE = 58, 42, 34
    cells = {".": 9, ",": 9, "+": 21, "×": 20}
    body, defs, kf = [], [], set()
    for i, (num, suffix, label, sub) in enumerate(METRICS):
        x = i * (TW + GAP)
        geo = f'x="{x + .75}" y=".75" width="{TW - 1.5}" height="{H - 1.5}" rx="12"'
        defs.append(f'<clipPath id="c{i}"><rect x="{x}" y="{BASE - 33}" width="{TW}" height="{STEP}"/></clipPath>')
        out = [f'<rect {geo} fill="$surface" stroke="$border"/>',
               f'<rect class="beam" style="animation-delay:{-i * 1.75:.2f}s" pathLength="100" {geo}/>']
        cx, col, digits = x + 20, 0, []
        for ch in num:
            if ch.isdigit():
                d = int(ch)
                seq = list(range(10)) + list(range(d + 1))
                last = len(seq) - 1
                kf.add(f"@keyframes r{last}{{from{{transform:translateY({last * STEP}px)}}}}")
                items = "".join(f'<text x="{n(cx + 10.75)}" y="{BASE + (k - last) * STEP}">{v}</text>'
                                for k, v in enumerate(seq))
                digits.append(f'<g class="roll" style="animation-name:r{last};'
                              f'animation-delay:{0.25 + i * 0.18 + col * 0.12:.2f}s">{items}</g>')
                cx += 21.5
                col += 1
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
        out.append(f'<text x="{x + 20}" y="88" font-size="13" font-weight="600" fill="$body">{esc(label)}</text>')
        out.append(f'<text x="{x + 20}" y="106" font-size="11.5" fill="$muted">{esc(sub)}</text>')
        body.append(f'<g class="up" style="animation-delay:{i * 0.1:.1f}s">{"".join(out)}</g>')
    css = SHARED_CSS + """
.beam{fill:none;stroke:url(#bm);stroke-width:1.5;stroke-linecap:round;stroke-dasharray:16 84;animation:beam 7s linear infinite}
@keyframes beam{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}
.roll{animation-duration:1.9s;animation-timing-function:cubic-bezier(.16,1,.3,1);animation-fill-mode:both}
""" + "\n".join(sorted(kf))
    defs.append('<linearGradient id="bm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$g1"/>'
                '<stop offset="1" stop-color="$g2"/></linearGradient>')
    label = "At a glance: " + "; ".join(f"{num}{suf} {lab} ({sub})" for num, suf, lab, sub in METRICS)
    return doc(W, H, label, css, "\n".join(defs), "\n".join(body), t)


# ── timeline ───────────────────────────────────────────────────────────────
def timeline(t):
    W, H = 840, 288
    X0, X1, T0, T1 = 218, 812, 2023.5, 2027.5
    AXIS = 248

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
    for i, (title, sub, start, end, key, tag, ongoing) in enumerate(ROWS):
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
        if ongoing:
            defs.append(f'<clipPath id="b{i}"><rect {geo}/></clipPath>')
            body.append(f'<g clip-path="url(#b{i})"><rect class="sweep" style="animation-delay:{1.5 + i * .5:.1f}s" '
                        f'x="{n(xs - 90)}" y="{cy - 11}" width="70" height="22" fill="url(#sw)"/></g>')
        inside = solid_end - xs > len(tag) * 6.6 + 20
        tx = xs + 10 if inside else solid_end + 9
        body.append(f'<text class="mono fade" style="animation-delay:{delay + .55:.2f}s" x="{n(tx)}" y="{cy + 3.5}" '
                    f'font-size="10.5" fill="{col}">{esc(tag)}</text>')
    # milestones
    body.append(f'<text x="24" y="{AXIS - 2}" font-size="12.5" font-weight="600" fill="$text">Milestones</text>')
    body.append(f'<text x="24" y="{AXIS + 13}" font-size="11" fill="$muted">awards · hackathons · launches</text>')
    body.append(f'<line x1="{X0}" x2="{X1}" y1="{AXIS}" y2="{AXIS}" stroke="$faint"/>')
    for i, (when, label, key, above) in enumerate(MILESTONES):
        x, delay = n(X(when)), 1.0 + i * 0.14
        body.append(f'<g transform="translate({x} {AXIS}) rotate(45)"><rect class="pop" style="animation-delay:{delay:.2f}s" '
                    f'x="-4.5" y="-4.5" width="9" height="9" rx="1.5" fill="${key}"/></g>')
        body.append(f'<text class="fade" style="animation-delay:{delay + .15:.2f}s" x="{x}" y="{AXIS - 13 if above else AXIS + 22}" '
                    f'font-size="10.5" font-weight="600" fill="$body" text-anchor="middle">{esc(label)}</text>')
    # now marker
    body.append(f'<line class="fade" style="animation-delay:1.2s" x1="{n(xn)}" x2="{n(xn)}" y1="40" y2="214" '
                f'stroke="$g1" stroke-width="1.2" stroke-dasharray="3 3"/>')
    body.append(f'<circle class="ring" stroke="$g1" cx="{n(xn)}" cy="40" r="3.5"/><circle cx="{n(xn)}" cy="40" r="3.5" fill="$g1"/>')
    body.append(f'<text class="mono" x="{n(xn - 12)}" y="43.5" font-size="10" fill="$a1" text-anchor="end">now</text>')
    css = SHARED_CSS + """
.grow{transform-box:fill-box;transform-origin:left center;animation:grow 1s cubic-bezier(.22,1,.36,1) both}
@keyframes grow{from{transform:scaleX(0)}}
.sweep{opacity:0;animation:sweep 4.5s linear infinite}
@keyframes sweep{0%{transform:translateX(0);opacity:1}70%{transform:translateX(720px);opacity:1}71%,100%{transform:translateX(720px);opacity:0}}
"""
    label = ("Timeline 2023–2027. " + " ".join(f"{title}: {sub}, {tag}." for title, sub, _, _, _, tag, _ in ROWS)
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
            body.append(
                f'<g class="up" style="animation-delay:{k * 0.05:.2f}s"><rect {geo} fill="$chip" stroke="$border"/>'
                f'<rect class="wave" style="animation-delay:{1.4 + k * 0.13:.2f}s" {geo}/>'
                f'<path transform="translate({x + 12} {y + 9}) scale({16 / 24:.4f})" fill="{colour}" d="{ICONS[slug]}"/>'
                f'<text x="{x + 36}" y="{y + 21.5}" font-size="13" font-weight="600" fill="$text">{esc(label)}</text></g>')
            x += w + 8
            k += 1
    css = SHARED_CSS + """
.wave{fill:none;stroke:url(#wv);stroke-width:1.5;opacity:0;animation:wave 7s ease-in-out infinite}
@keyframes wave{0%{opacity:0}5%{opacity:1}14%{opacity:0}100%{opacity:0}}
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
@keyframes hit{0%{transform:scale(1);opacity:.9}14%{transform:scale(3);opacity:0}100%{transform:scale(3);opacity:0}}
"""
    label = "Merged pull requests. " + " ".join(
        f"{repo}: {len(prs)} merged ({', '.join('#' + str(p) for p in prs)})." for repo, _, _, prs in OSS)
    return doc(W, H, label, css, "", "\n".join(body), t)


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
    css = SHARED_CSS + art_css + """
.gl{animation:gl 10s ease-in-out infinite}
@keyframes gl{0%,100%{transform:translate(0,0)}50%{transform:translate(-18px,8px)}}
"""
    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$card1"/><stop offset="1" stop-color="$card2"/></linearGradient>
<radialGradient id="ga"><stop offset="0" stop-color="{col}" stop-opacity="$glowop"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="12"/></clipPath>
"""
    body = f"""
<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>
<g clip-path="url(#card)"><circle class="gl" cx="340" cy="50" r="150" fill="url(#ga)"/>{art}</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="11.5" fill="none" stroke="$border"/>
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

    css = SHARED_CSS + """
.w{fill:none;stroke-width:1.4}
.w1{animation:w1 9s linear infinite}
.w2{animation:w2 13s linear infinite}
.w3{animation:w1 17s linear infinite reverse}
@keyframes w1{to{transform:translateX(240px)}}
@keyframes w2{to{transform:translateX(-180px)}}
.d1{animation:drift 14s ease-in-out infinite}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(30px,-10px)}}
"""
    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$card1"/><stop offset="1" stop-color="$card2"/></linearGradient>
<radialGradient id="ga"><stop offset="0" stop-color="$g1" stop-opacity="$glowop"/><stop offset="1" stop-color="$g1" stop-opacity="0"/></radialGradient>
<linearGradient id="hl" gradientUnits="userSpaceOnUse" x1="455" y1="0" x2="725" y2="0"><stop offset="0" stop-color="$g1"/><stop offset="1" stop-color="$g2"/></linearGradient>
<linearGradient id="wf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="$g1" stop-opacity="0"/><stop offset=".5" stop-color="$g2" stop-opacity=".7"/><stop offset="1" stop-color="$g1" stop-opacity="0"/></linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
"""
    body = f"""
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<g clip-path="url(#card)">
<circle class="d1" cx="420" cy="210" r="300" fill="url(#ga)"/>
<path class="w w1" stroke="$g1" stroke-opacity=".5" d="{wave(132, 9, 240)}"/>
<path class="w w2" stroke="$g2" stroke-opacity=".4" d="{wave(140, 12, 180)}"/>
<path class="w w3" stroke="$edge" stroke-opacity=".35" d="{wave(148, 7, 240)}"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="$border"/>
<g class="up"><text x="420" y="66" font-size="30" font-weight="800" letter-spacing="-.4" fill="$text" text-anchor="middle">Let’s build something <tspan fill="url(#hl)">production-ready.</tspan></text></g>
<g class="up" style="animation-delay:.15s"><text x="420" y="97" font-size="14" fill="$muted" text-anchor="middle">Open to software engineering internships and full-time roles · 2027 grad</text></g>
"""
    return doc(W, H, "Let's build something production-ready. Open to software engineering internships and "
               "full-time roles, 2027 grad.", css, defs, body, t)


# ── divider + buttons ──────────────────────────────────────────────────────
def divider(t):
    W, H = 840, 12
    css = """
.g{animation:run 6s cubic-bezier(.45,0,.55,1) infinite}
@keyframes run{from{transform:translateX(-160px)}to{transform:translateX(840px)}}
"""
    defs = """
<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="$border" stop-opacity="0"/><stop offset=".5" stop-color="$border"/><stop offset="1" stop-color="$border" stop-opacity="0"/></linearGradient>
<linearGradient id="gl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="$g1" stop-opacity="0"/><stop offset=".5" stop-color="$g2"/><stop offset="1" stop-color="$g1" stop-opacity="0"/></linearGradient>
"""
    body = f"""
<rect y="5.5" width="{W}" height="1" fill="url(#ln)"/>
<rect class="g" y="5" width="160" height="2" rx="1" fill="url(#gl)"/>
"""
    return doc(W, H, "", css, defs, body, t)


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


def button(t, label, width, glyph, primary):
    H = 36
    if primary:
        fill, stroke, ink, icon = "url(#p)", "none", "$onaccent", "$onaccent"
    else:
        fill, stroke, ink, icon = "$surface", "$border", "$text", "$a1"
    if glyph == "gitlab":
        g = f'<path transform="translate(14 10) scale({16 / 24:.4f})" fill="{icon}" d="{ICONS["gitlab"]}"/>'
    else:
        bg = "$g1" if primary else "$surface"
        g = f'<g transform="translate(14 10)">{GLYPHS[glyph].format(c=icon, bg=bg)}</g>'
    css = """
.s{opacity:0;animation:s 5s ease-in-out 1s infinite}
@keyframes s{0%{transform:translateX(0);opacity:0}8%{opacity:1}34%{transform:translateX(200px);opacity:1}38%,100%{transform:translateX(200px);opacity:0}}
"""
    defs = f"""
<linearGradient id="p" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="$g1"/><stop offset="1" stop-color="$g2"/></linearGradient>
<linearGradient id="sg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="b"><rect width="{width}" height="{H}" rx="10"/></clipPath>
"""
    shine = ('<g clip-path="url(#b)"><g transform="skewX(-20)"><rect class="s" x="-40" width="34" height="36" '
             'fill="url(#sg)"/></g></g>') if primary else ""
    body = f"""
<rect x=".5" y=".5" width="{width - 1}" height="{H - 1}" rx="9.5" fill="{fill}" stroke="{stroke}"/>{shine}
{g}<text x="38" y="22.7" font-size="13" font-weight="600" fill="{ink}">{esc(label)}</text>
"""
    return doc(width, H, label, css, defs, body, t)


def main():
    OUT.mkdir(exist_ok=True)
    files = {}
    for theme, t in THEMES.items():
        files[f"hero-{theme}.svg"] = hero(t)
        files[f"metrics-{theme}.svg"] = metrics(t)
        files[f"timeline-{theme}.svg"] = timeline(t)
        files[f"opensource-{theme}.svg"] = opensource(t)
        files[f"stack-{theme}.svg"] = stack(t, theme)
        files[f"footer-{theme}.svg"] = footer(t)
        files[f"divider-{theme}.svg"] = divider(t)
    # Linked images get a single dark version: GitHub rewrites <a><picture>…</picture></a> so the
    # link ends up pointing at the image file, which rules out theme switching for anything clickable.
    dark = THEMES["dark"]
    for slug in COVERS:
        files[f"cover-{slug}.svg"] = cover(dark, slug)
    for slug, label, width, glyph, primary in BUTTONS:
        files[f"btn-{slug}.svg"] = button(dark, label, width, glyph, primary)
    for name, svg in sorted(files.items()):
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"{len(svg.encode()) / 1024:6.1f} KB  assets/{name}")


if __name__ == "__main__":
    main()
