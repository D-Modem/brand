#!/usr/bin/env python3
"""Makes a repository's README banner and social preview, and puts the banner in its checkout.

Writes banner/<name>.svg, .png, @2x.png (1280x320) and social/<name>.svg, .png (1280x640).

    python3 tools/art.py                            every repository's banner and social preview
    python3 tools/art.py menu bbs                   just those
    python3 tools/art.py menu --only social         only the social preview (or --only banner)
    python3 tools/art.py menu --install ../menu     and copy the banner to ../menu/.github/banner.png,
                                                    adding it to the top of ../menu/README.md
    python3 tools/art.py foo --book Beige --tag "What foo is" --sub "One more line." \
        --icon wave --chips Go,SIP                  a repository not in tools/gen.py yet

"suite" is the organization's own banner and social preview. Social previews are uploaded by hand:
docs/assets.md.

The taglines, colours and icons of the known repositories are in REPOS at the top of tools/gen.py;
a new repository belongs there too, so its social preview matches. Needs node with Playwright and
Sauce Code Pro (SauceCodePro Nerd Font Mono) installed, as for tools/render.js.
"""
import argparse, os, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen  # noqa: E402

# the free Rainbow Books, for repositories not in gen.REPOS yet
FREE = {"Beige": "#d9c7a0", "White": "#f2f4fa"}
ICONS = ["wave", "mark", "phone", "chip", "bbs", "3270", "menu", "gui", "books"]


def install(name, repo):
    """Copy the @2x banner into repo/.github/banner.png and show it above the README's title."""
    gh = os.path.join(repo, ".github")
    os.makedirs(gh, exist_ok=True)
    shutil.copyfile(os.path.join(gen.ROOT, "banner", f"{name}@2x.png"), os.path.join(gh, "banner.png"))
    readme = os.path.join(repo, "README.md")
    text = open(readme).read() if os.path.exists(readme) else f"# {name}\n"
    if ".github/banner.png" not in text:
        r = gen.REPOS.get(name, gen.SUITE)
        alt = "D-Modem" if name == "suite" else f"D-Modem/{name}"
        text = f'<img src=".github/banner.png" alt="{alt}: {r["tag"]}" width="100%">\n\n' + text
        open(readme, "w").write(text)
    print(f"{name}: {gh}/banner.png")


def parser():
    """art.py's command line (also docs/reference.md's, by tools/brand_ref.py)."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="repositories (default: all, and suite)")
    ap.add_argument("--install", metavar="REPO_DIR", help="copy the banner into this checkout and its README (one name)")
    ap.add_argument("--book", help="Rainbow Book for a new repository: " + ", ".join(
        [n for n, _, _ in gen.BOOKS] + list(FREE)))
    ap.add_argument("--color", help="accent colour instead of a Book's, e.g. #d9c7a0")
    ap.add_argument("--tag", help="the coloured tagline")
    ap.add_argument("--sub", help="the muted line under it")
    ap.add_argument("--icon", choices=ICONS, default="wave", help="the repository's icon (default: wave)")
    ap.add_argument("--chips", default="", help="comma-separated tags on the social preview, e.g. Go,PAM")
    ap.add_argument("--only", choices=["banner", "social"], help="make only one of the two")
    return ap


def main():
    ap = parser()
    a = ap.parse_args()

    names = a.names or list(gen.REPOS) + ["suite"]
    for n in names:
        if n == "suite" or n in gen.REPOS:
            continue
        if not a.tag:
            ap.error(f"{n} is not in tools/gen.py REPOS: give --tag (and --sub, --book or --color, --icon, --chips)")
        book = a.book or "Beige"
        color = a.color or gen.BOOK.get(book, (None, None))[1] or FREE.get(book)
        if not color:
            ap.error(f"unknown Book {book}")
        gen.REPOS[n] = dict(book=book, color=color, icon=a.icon, tag=a.tag, sub=a.sub or "",
                          chips=[c.strip() for c in a.chips.split(",") if c.strip()])
    if a.install and (len(names) != 1 or a.only == "social"):
        ap.error("--install takes one name, and the banner")

    svgs = []
    for n in names:
        if a.only != "social":
            gen.write(f"banner/{n}.svg", gen.banner(n, gen.SUITE if n == "suite" else gen.REPOS[n]))
            svgs.append(f"banner/{n}.svg")
        if a.only != "banner":
            gen.write(f"social/{n}.svg", gen.social(n, gen.SUITE if n == "suite" else gen.REPOS[n]))
            svgs.append(f"social/{n}.svg")
    subprocess.run(["node", os.path.join(gen.ROOT, "tools", "render.js"), *svgs], check=True)
    for rel in svgs:
        print(rel.replace(".svg", ".png") + (" " + rel.replace(".svg", "@2x.png") if rel.startswith("banner") else ""))
    if a.install:
        install(names[0], a.install)


if __name__ == "__main__":
    main()
