#!/usr/bin/env python3
"""The app's launcher icon: an RJ11 jack striped in the Rainbow Book colours, the white carrier inside.
Drawn on Android's 108-unit adaptive icon canvas (launchers show the middle 72, keep art within 21..87)."""
import os
from gen import ROOT, BOOKS, BG, INK, wave_path

X, Y, W, H = 34, 34, 40, 32           # the jack opening; the latch notch hangs below it


def jack_d():
    nx, nh, cx = W * 0.4, H * 0.3, X + W / 2
    return f"M{X},{Y} H{X + W} V{Y + H} H{cx + nx / 2} V{Y + H + nh} H{cx - nx / 2} V{Y + H} H{X} Z"


def icon(size=432, view="0 0 108 108"):
    stops = "".join(f'<stop offset="{i / 6:.4f}" stop-color="{c}"/><stop offset="{(i + 1) / 6:.4f}" stop-color="{c}"/>'
                    for i, (_, _, c) in enumerate(BOOKS))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="{view}">
<defs><linearGradient id="stripes" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient></defs>
<rect x="-10" y="-10" width="128" height="128" fill="{BG}"/>
<path d="{jack_d()}" fill="none" stroke="url(#stripes)" stroke-width="3.4"/>
<path d="{wave_path(39, 69, 50, 6, 2.5, 0.5)}" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "app-icon"), exist_ok=True)
    with open(os.path.join(ROOT, "app-icon", "ic_launcher.svg"), "w") as f:
        f.write(icon() + "\n")
    # Play Store listing icon: 512px of the 72 units a launcher shows (Play applies its own mask)
    with open(os.path.join(ROOT, "app-icon", "play-store.svg"), "w") as f:
        f.write(icon(512, "18 18 72 72") + "\n")
