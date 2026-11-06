#!/usr/bin/env python3
"""docs/reference.md from the code: each repository's Book, colour, icon and
taglines (REPOS in tools/gen.py), the palette, and tools/art.py's command
line. It also checks that the sites' theme (pages/theme/main.html) gives
each repository the colour gen.py does.

    python3 tools/brand_ref.py           writes the page
    python3 tools/brand_ref.py --check   exit 1 if it is out of date, or the theme disagrees
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art  # noqa: E402
import gen  # noqa: E402

OUT = os.path.join(gen.ROOT, "docs", "reference.md")
THEME = os.path.join(gen.ROOT, "pages", "theme", "main.html")


def cell(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return " ".join(s.replace("|", "\\|").split())


def swatch(color):
    return '<span class="suite-swatch" style="background:%s"></span> `%s`' % (color, color)


def theme_problems():
    text = open(THEME, encoding="utf-8").read()
    m = re.search(r"set books = \{(.*?)\}", text, re.S)
    books = dict(re.findall(r'"([^"]+)":\s*"(#[0-9a-fA-F]{6})"', m.group(1))) if m else {}
    out = []
    for name, r in gen.REPOS.items():
        if books.get(name, "").lower() != r["color"].lower():
            out.append("pages/theme/main.html gives %s %s, tools/gen.py %s"
                       % (name, books.get(name, "no colour"), r["color"]))
    return out


def usage():
    rows = []
    for a in art.parser()._actions:
        if isinstance(a, argparse._HelpAction):
            continue
        if a.option_strings:
            name = ", ".join("`%s`" % o for o in a.option_strings)
            arg = "" if a.nargs == 0 else (a.metavar or a.dest.upper())
        else:
            name, arg = "`%s`" % a.dest, "..." if a.nargs == "*" else ""
        choices = ", ".join("`%s`" % c for c in a.choices) if a.choices else ""
        help_text = a.help or ""
        help_text = help_text[0].upper() + help_text[1:]
        if choices:
            help_text += " (%s)" % choices
        rows.append("| %s | %s | %s |\n" % (name, cell(arg), cell(help_text)))
    return rows


def page():
    b = ["<!-- Made by tools/brand_ref.py from tools/gen.py and tools/art.py: "
         "change the code (or the script), not this page. -->\n\n",
         "# Reference\n\n",
         "The suite's colours and each repository's art, as `tools/gen.py` "
         "draws them, and `tools/art.py`'s command line. "
         "[Palette, type and the app icon](palette.md) says why they are so; "
         "[Assets](assets.md) how to make the images.\n\n",
         "## Repositories\n\n",
         "Each repository's Rainbow Book is its accent: on its banner, its "
         "social preview and its site.\n\n",
         "| repository | Book | colour | icon | tagline | second line | tags |\n",
         "|---|---|---|---|---|---|---|\n"]
    for name, r in list(gen.REPOS.items()) + [("suite", gen.SUITE)]:
        fmt = gen.BOOK.get(r["book"], (None,))[0]
        book = r["book"] + (" (%s)" % fmt if fmt else "")
        b.append("| `%s` | %s | %s | `%s` | %s | %s | %s |\n" % (
            name, book, swatch(r["color"]), r["icon"], cell(r["tag"]), cell(r["sub"]),
            ", ".join(r.get("chips", []))))
    b += ["\n`suite` is the organization's own banner and social preview (its "
          "profile and website), the mark in all six Books.\n\n",
          "## Palette\n\n",
          "### Rainbow Books\n\n",
          "| Book | format | colour |\n|---|---|---|\n"]
    for n, fmt, c in gen.BOOKS:
        b.append("| %s | %s | %s |\n" % (n, fmt, swatch(c)))
    b += ["\nThe free Books, for a repository not given one yet "
          "(`tools/art.py --book`):\n\n",
          "| Book | colour |\n|---|---|\n"]
    for n, c in art.FREE.items():
        b.append("| %s | %s |\n" % (n, swatch(c)))
    b += ["\n### The rest\n\n", "| name | colour | use |\n|---|---|---|\n"]
    for n, use in (("BG", "background"), ("BG2", "the background's second shade"),
                   ("INK", "text"), ("DIM", "muted text"), ("GREEN", "the carrier, and the suite's own accent")):
        b.append("| `%s` | %s | %s |\n" % (n, swatch(getattr(gen, n)), use))
    b += ["\nType: %s.\n\n" % cell(gen.FONT.replace("'", "")),
          "## tools/art.py\n\n",
          "Makes a repository's banner and social preview, and puts the banner "
          "in its checkout.\n\n",
          "    python3 tools/art.py [names...] [options]\n\n",
          "| argument | value | what it does |\n|---|---|---|\n"]
    b += usage()
    return "".join(b)


def main():
    problems = theme_problems()
    text = page()
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
    if "--check" in sys.argv[1:]:
        if old != text:
            problems.append("docs/reference.md is out of date: run python3 tools/brand_ref.py")
    elif old != text:
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(text)
    for p in problems:
        print("brand_ref: " + p, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
