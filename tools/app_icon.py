#!/usr/bin/env python3
"""The app's launcher icon: an RJ11 jack striped in the Rainbow Book colours, the white carrier inside.
Drawn on Android's 108-unit adaptive icon canvas (launchers show the middle 72, keep art within 21..87)."""
import os
from gen import ROOT, BG, app_icon_art


def icon(size=432, view="0 0 108 108"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="{view}">
<rect x="-10" y="-10" width="128" height="128" fill="{BG}"/>
{app_icon_art()}
</svg>'''


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "app-icon"), exist_ok=True)
    with open(os.path.join(ROOT, "app-icon", "ic_launcher.svg"), "w") as f:
        f.write(icon() + "\n")
    # Play Store listing icon: 512px of the 72 units a launcher shows (Play applies its own mask)
    with open(os.path.join(ROOT, "app-icon", "play-store.svg"), "w") as f:
        f.write(icon(512, "18 18 72 72") + "\n")
