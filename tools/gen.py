#!/usr/bin/env python3
"""Generates the D-Modem org avatar and repo social preview SVGs."""
import math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG, BG2, INK, DIM = "#0a0f1c", "#121a2e", "#e8f0ff", "#7f8bab"
FONT = "'SauceCodePro Nerd Font Mono', 'Source Code Pro', monospace"
GREEN = "#3dff9a"
# The CD "Rainbow Books", in rainbow order: (name, format, colour).
BOOKS = [("Red", "CD-DA", "#ff4d5e"), ("Orange", "CD-R/RW", "#ff8a3d"), ("Yellow", "CD-ROM", "#ffd23d"),
         ("Green", "CD-i", "#3ddc84"), ("Blue", "CD Extra", "#3d8bff"), ("Purple", "DDCD", "#a66bff")]
BOOK = {n: (y, c) for n, y, c in BOOKS}

REPOS = {
    "D-Modem":  dict(book="Red", color=BOOK["Red"][1],     icon="wave",
                     tag="V.92 softmodem over SIP", sub="No modem hardware. V.92 / V.90 / V.34 / fax.",
                     chips=["C++", "SIP", "Asterisk", "FreeSWITCH"]),
    "app":      dict(book="Yellow", color=BOOK["Yellow"][1], icon="phone",
                     tag="A dial-up modem in your pocket", sub="Android app: V.92 over a SIP call.",
                     chips=["Android", "Kotlin", "NDK", "V.92"]),
    "hardware": dict(book="Orange", color=BOOK["Orange"][1], icon="chip",
                     tag="pico-serial", sub="RP2040 serial and phone-line USB sticks.",
                     chips=["RP2040", "DB25", "USB-C", "CERN-OHL-S"]),
    "bbs":      dict(book="Blue", color=BOOK["Blue"][1], icon="bbs",
                     tag="A bulletin board for every caller", sub="Telnet, TN3270 and modem callers, in Go.",
                     chips=["Go", "ANSI", "TN3270", "Doors"]),
    "go3270":   dict(book="Purple", color=BOOK["Purple"][1], icon="3270",
                     tag="Go servers for 3270 terminals", sub="Build TN3270 data streams from fields.",
                     chips=["Go", "TN3270", "EBCDIC"]),
    "menu":     dict(book="Green", color=BOOK["Green"][1], icon="menu",
                     tag="modemmenu", sub="Login and menu for dial-up callers.",
                     chips=["Go", "PAM", "LDAP", "SQL", "PPP"]),
    # the White Book (Video CD), one of the free ones, for the brand itself
    "brand":    dict(book="White", color="#f2f4fa", icon="books",
                     tag="Logos, colours and type", sub="The mark, the Rainbow Books, Sauce Code Pro.",
                     chips=["SVG", "PNG", "Rainbow Books", "Sauce Code Pro"]),
}


def wave_path(x0, x1, y, amp, cycles, analog_frac=0.55):
    """Sine on the left turning into square pulses on the right: analog to digital."""
    pts, w = [], x1 - x0
    xa = x0 + w * analog_frac
    n = 120
    for i in range(n + 1):
        x = x0 + (xa - x0) * i / n
        t = (x - x0) / w * cycles * 2 * math.pi
        pts.append(f"{x:.1f},{y - amp * math.sin(t):.1f}")
    d = "M" + " L".join(pts)
    # square part continues phase
    # analog_frac * cycles should end on a peak (k + 0.25) so the pulses join cleanly
    per = w / cycles
    x, level, step = xa, 1, per / 4
    while x < x1:
        nx = min(x + step, x1)
        step = per / 2
        d += f" H{nx:.1f}"
        if nx < x1:
            level = -level
            d += f" V{y - amp * level:.1f}"
        x = nx
    return d


def mark(size, color="url(#books)", bg=True, wave=INK):
    """The D-Modem mark in a size x size box: a D with a sine-to-square carrier."""
    s = size / 500
    g = []
    if bg:
        g.append(f'<rect width="{size}" height="{size}" fill="{BG}"/>')
        g.append(f'<rect width="{size}" height="{size}" fill="url(#qam)" opacity="0.9"/>')
    g.append(f'<g transform="scale({s})">')
    g.append(f'<path d="M140 100 H240 A150 150 0 0 1 240 400 H140 Z" fill="none" stroke="{color}" '
             f'stroke-width="38" stroke-linejoin="round" filter="url(#glow)"/>')
    g.append(f'<path d="{wave_path(178, 362, 250, 56, 2.5, 0.5)}" fill="none" stroke="{wave}" stroke-width="16" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    g.append('</g>')
    return "\n".join(g)


def defs(color=GREEN, w=500, h=500):
    n = len(BOOKS)
    stops = "".join(f'<stop offset="{i / n:.4f}" stop-color="{c}"/><stop offset="{(i + 1) / n:.4f}" stop-color="{c}"/>'
                    for i, (_, _, c) in enumerate(BOOKS))
    # faint QAM constellation dots as a background texture (a nod to V.34 / V.92)
    return f'''<defs>
  <pattern id="qam" width="28" height="28" patternUnits="userSpaceOnUse">
    <circle cx="14" cy="14" r="1.6" fill="{color}" opacity="0.13"/>
  </pattern>
  <radialGradient id="vig" cx="50%" cy="45%" r="75%">
    <stop offset="0" stop-color="{color}" stop-opacity="0.10"/>
    <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vig2" gradientUnits="userSpaceOnUse" cx="280" cy="320" r="520">
    <stop offset="0" stop-color="{color}" stop-opacity="0.12"/>
    <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="books" gradientUnits="userSpaceOnUse" x1="0" y1="81" x2="0" y2="419">{stops}</linearGradient>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="6" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>'''


def avatar():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" viewBox="0 0 500 500">
{defs("#9fb0d8")}
<rect width="500" height="500" fill="{BG}"/>
<rect width="500" height="500" fill="url(#qam)"/>
<rect width="500" height="500" fill="url(#vig)"/>
{mark(500, bg=False)}
</svg>'''


# The app's launcher icon (tools/app_icon.py): an RJ11 jack on the 108-unit adaptive icon canvas.
JACK_X, JACK_Y, JACK_W, JACK_H = 34, 34, 40, 32


def jack_d():
    nx, nh, cx = JACK_W * 0.4, JACK_H * 0.3, JACK_X + JACK_W / 2
    return (f"M{JACK_X},{JACK_Y} H{JACK_X + JACK_W} V{JACK_Y + JACK_H} H{cx + nx / 2} V{JACK_Y + JACK_H + nh} "
            f"H{cx - nx / 2} V{JACK_Y + JACK_H} H{JACK_X} Z")


def app_icon_art(gid="stripes"):
    """The jack, striped in the Rainbow Book colours, with the white carrier inside (108-unit canvas)."""
    stops = "".join(f'<stop offset="{i / 6:.4f}" stop-color="{c}"/><stop offset="{(i + 1) / 6:.4f}" stop-color="{c}"/>'
                    for i, (_, _, c) in enumerate(BOOKS))
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient></defs>'
            f'<path d="{jack_d()}" fill="none" stroke="url(#{gid})" stroke-width="3.4"/>'
            f'<path d="{wave_path(39, 69, 50, 6, 2.5, 0.5)}" fill="none" stroke="{INK}" stroke-width="3.4" '
            'stroke-linecap="round" stroke-linejoin="round"/>')


def icon(kind, c):
    """Repo icon drawn in a 300x300 box."""
    sw = 'stroke-width="14" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    if kind == "wave":
        return mark(300, c, bg=False)
    if kind == "phone":
        return f'''<rect x="80" y="20" width="140" height="260" rx="26" stroke="{c}" {sw} filter="url(#glow)"/>
<line x1="130" y1="48" x2="170" y2="48" stroke="{c}" {sw}/>
<g transform="translate(150 146) scale(2.1) translate(-54 -54.8)">{app_icon_art("appjack")}</g>
<circle cx="150" cy="248" r="9" fill="{c}"/>'''
    if kind == "chip":
        pins = "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="70" stroke="{c}" {sw}/><line x1="{x}" y1="230" x2="{x}" y2="260" stroke="{c}" {sw}/>'
                       for x in (100, 150, 200))
        pins += "".join(f'<line x1="40" y1="{y}" x2="70" y2="{y}" stroke="{c}" {sw}/><line x1="230" y1="{y}" x2="260" y2="{y}" stroke="{c}" {sw}/>'
                        for y in (100, 150, 200))
        return f'''<rect x="70" y="70" width="160" height="160" rx="18" stroke="{c}" {sw} filter="url(#glow)"/>
{pins}
<path d="M90 134 H118 M90 166 H118 M174 150 H210" stroke="{INK}" stroke-width="9" fill="none" stroke-linecap="round"/>
<path d="M118 116 H140 A34 34 0 0 1 140 184 H118 Z" stroke="{INK}" stroke-width="10" fill="none" stroke-linejoin="round"/>
<circle cx="90" cy="134" r="8" fill="{INK}"/><circle cx="90" cy="166" r="8" fill="{INK}"/><circle cx="210" cy="150" r="8" fill="{INK}"/>'''
    if kind == "bbs":
        bars = [col for _, _, col in BOOKS]
        b = "".join(f'<rect x="{62 + i * 30}" y="196" width="26" height="22" fill="{col}"/>' for i, col in enumerate(bars))
        return f'''<rect x="30" y="50" width="240" height="200" rx="18" stroke="{c}" {sw} filter="url(#glow)"/>
<line x1="30" y1="88" x2="270" y2="88" stroke="{c}" stroke-width="10"/>
<circle cx="56" cy="69" r="6" fill="{c}"/><circle cx="76" cy="69" r="6" fill="{c}"/><circle cx="96" cy="69" r="6" fill="{c}"/>
<text x="62" y="140" font-family="{FONT}" font-weight="800" font-size="34" fill="{INK}">BBS<tspan fill="{c}">_</tspan></text>
<text x="62" y="178" font-family="{FONT}" font-size="20" fill="{DIM}">[M]sg [F]iles</text>
{b}'''
    if kind == "3270":
        rows = ""
        for i, (lab, w) in enumerate([("USERID", 90), ("PASSWD", 90), ("CMD ==>", 100)]):
            y = 120 + i * 38
            rows += f'<text x="56" y="{y}" font-family="{FONT}" font-size="20" font-weight="700" fill="{INK}">{lab}</text>'
            rows += f'<line x1="{160}" y1="{y + 4}" x2="{160 + w}" y2="{y + 4}" stroke="{c}" stroke-width="5"/>'
        return f'''<rect x="30" y="40" width="240" height="190" rx="14" stroke="{c}" {sw} filter="url(#glow)"/>
<text x="56" y="84" font-family="{FONT}" font-size="18" fill="{c}">TN3270  ===</text>
{rows}
<path d="M120 230 L105 268 H195 L180 230" stroke="{c}" {sw}/>
'''
    if kind == "menu":
        return f'''<rect x="30" y="40" width="240" height="220" rx="18" stroke="{c}" {sw} filter="url(#glow)"/>
<text x="56" y="96" font-family="{FONT}" font-size="26" font-weight="700" fill="{INK}">login: <tspan fill="{c}">_</tspan></text>
<text x="56" y="138" font-family="{FONT}" font-size="22" fill="{c}">1) BBS</text>
<text x="56" y="172" font-family="{FONT}" font-size="22" fill="{DIM}">2) PPP</text>
<text x="56" y="206" font-family="{FONT}" font-size="22" fill="{DIM}">3) Shell</text>
'''
    if kind == "books":
        # the six Rainbow Books standing on a shelf, each spine banded like a book's
        spines = ""
        for i, (_, _, col) in enumerate(BOOKS):
            x, top = 46 + i * 36, 58 + (i % 3) * 10
            spines += (f'<rect x="{x}" y="{top}" width="30" height="{240 - top}" rx="4" fill="{col}"/>'
                       f'<rect x="{x}" y="{top + 18}" width="30" height="5" fill="{BG}" fill-opacity="0.45"/>'
                       f'<rect x="{x}" y="{208}" width="30" height="5" fill="{BG}" fill-opacity="0.45"/>')
        return f'''{spines}
<rect x="30" y="240" width="240" height="12" rx="6" fill="{c}"/>'''
    raise ValueError(kind)


def social(name, r):
    c = r["color"]
    chips, x = [], 560
    for t in r["chips"]:
        w = 24 + len(t) * 15
        chips.append(f'<rect x="{x}" y="452" width="{w}" height="44" rx="22" fill="none" stroke="{c}" stroke-opacity="0.6" stroke-width="2"/>'
                     f'<text x="{x + w / 2}" y="481" text-anchor="middle" font-family="{FONT}" font-size="22" fill="{INK}">{t}</text>')
        x += w + 14
    size = 104 if len(name) <= 6 else 92
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">
{defs(c)}
<rect width="1280" height="640" fill="{BG}"/>
<rect width="1280" height="640" fill="url(#qam)"/>
<rect width="1280" height="640" fill="url(#vig2)"/>
<rect x="100" y="140" width="360" height="360" rx="40" fill="{BG2}" stroke="{c}" stroke-opacity="0.35" stroke-width="2"/>
<g transform="translate(130 170)">{icon(r["icon"], c)}</g>
<g transform="translate(560 128)">{mark(64, bg=False)}</g>
<text x="640" y="172" font-family="{FONT}" font-size="30" fill="{DIM}">D-Modem /</text>
<text x="556" y="290" font-family="{FONT}" font-weight="800" font-size="{size}" fill="{INK}">{name}</text>
<text x="560" y="350" font-family="{FONT}" font-weight="700" font-size="34" fill="{c}">{r["tag"]}</text>
<text x="560" y="400" font-family="{FONT}" font-size="26" fill="{DIM}">{r["sub"]}</text>
{"".join(chips)}
<rect x="0" y="0" width="34" height="640" fill="{c}"/>
<text transform="translate(24 320) rotate(-90)" text-anchor="middle" font-family="{FONT}" font-weight="800" font-size="17" letter-spacing="3" fill="{BG}">D-Modem/{name}</text>
<path d="{wave_path(0, 1280, 600, 10, 16, 0.578125)}" fill="none" stroke="{c}" stroke-opacity="0.35" stroke-width="3"/>
</svg>'''


def mark_only():
    """The mark on a transparent background, for READMEs and docs."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" viewBox="0 0 500 500">
{defs()}
{mark(500, bg=False, wave=DIM)}
</svg>'''


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    write("avatar/org-avatar.svg", avatar())
    write("avatar/mark.svg", mark_only())
    for n, r in REPOS.items():
        write(f"social/{n}.svg", social(n, r))
