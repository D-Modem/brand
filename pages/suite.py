#!/usr/bin/env python3
# The list of the suite's core repositories (pages/suite.yml) in a site.
# tools/site.sh runs it after it copies the theme into REPO_DIR/.site/:
#
#   python3 suite.py base REPO_DIR    the list goes into
#       .site/mkdocs-base.yml as extra.suite, for the bar and the accent
#       of the theme (pages/theme/partials/suite.html, main.html);
#   python3 suite.py cards REPO_DIR   each "<!-- suite:cards -->" line in
#       the pages of .site/docs/ becomes the grid of cards of the suite.
#
# .github/workflows/sites.yml runs it to know which sites to build again:
#
#   python3 suite.py sites            a JSON list of the repositories
#       (D-Modem/<name>) whose sites use the list: each core repository
#       but brand, and D-Modem.github.io.
#
# A site that has a "<!-- suite:cards -->" line must build from the copy
# of docs/ (docs_dir: .site/docs in mkdocs.yml). Thus the build does not
# change the files in docs/.
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
LIST = os.path.join(HERE, "suite.yml")
MARKER = re.compile(r"^[ \t]*<!--\s*suite:cards\s*-->[ \t]*$", re.M)
COLOUR = re.compile(r"^#[0-9a-fA-F]{6}$")
NAME = re.compile(r"^[A-Za-z0-9._-]+$")


# Read pages/suite.yml and return its list of repositories. Stop with an
# error if an entry has a missing or incorrect key, or a name is in the
# list two times.
def load(path=LIST):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    repos = data.get("repos")
    if not isinstance(repos, list) or not repos:
        sys.exit("suite: %s has no repos list" % path)
    seen = set()
    for i, r in enumerate(repos):
        where = "%s: repos[%d]" % (path, i)
        if not isinstance(r, dict):
            sys.exit("suite: %s is not a mapping" % where)
        for key in ("name", "title", "colour", "card"):
            if not isinstance(r.get(key), str) or not r[key].strip():
                sys.exit("suite: %s has no %s" % (where, key))
        if not NAME.match(r["name"]):
            sys.exit("suite: %s: %r is not a repository name" % (where, r["name"]))
        if not COLOUR.match(r["colour"]):
            sys.exit("suite: %s: colour %r is not #rrggbb" % (where, r["colour"]))
        if r["name"].lower() in seen:
            sys.exit("suite: %s: %s is in the list two times" % (where, r["name"]))
        seen.add(r["name"].lower())
    return repos


# Return the text of mkdocs-base.yml with extra.suite added: the name,
# title and colour of each repository, as JSON (JSON is also YAML).
def with_suite(base, repos):
    bar = [{"name": r["name"], "title": r["title"], "colour": r["colour"].lower()} for r in repos]
    line = "  suite: %s\n" % json.dumps(bar)
    new, n = re.subn(r"^extra:[ \t]*\n", lambda m: m.group(0) + line, base, count=1, flags=re.M)
    if n != 1:
        sys.exit("suite: mkdocs-base.yml has no extra: block")
    return new


# Return the Markdown of the grid of cards: one card for each repository,
# its name a link to the repository on GitHub.
def cards(repos):
    out = ['<div class="grid cards" markdown>', ""]
    for r in repos:
        out += ["-   **[%s](https://github.com/D-Modem/%s)**" % (r["name"], r["name"]), "", "    ---", ""]
        out += [("    " + l).rstrip() for l in r["card"].strip().splitlines()]
        out.append("")
    out.append("</div>")
    return "\n".join(out)


# Put extra.suite into REPO_DIR/.site/mkdocs-base.yml.
def cmd_base(repo, repos):
    path = os.path.join(repo, ".site", "mkdocs-base.yml")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(with_suite(text, repos))


# Replace each marker line in the pages of REPO_DIR/.site/docs/ with the
# grid of cards.
def cmd_cards(repo, repos):
    grid = cards(repos)
    for d, _, files in os.walk(os.path.join(repo, ".site", "docs")):
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(d, name)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            new = MARKER.sub(lambda m: grid, text)
            if new != text:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)


# Return the repositories whose sites must be built again when the list
# or the theme changes. brand is not in it: its own Pages workflow builds
# its site on each push to main.
def sites(repos):
    out = ["D-Modem/" + r["name"] for r in repos if r["name"] != "brand"]
    return out + ["D-Modem/D-Modem.github.io"]


# Read the command line and do the command.
def main():
    repos = load()
    if sys.argv[1:] == ["sites"]:
        print(json.dumps(sites(repos)))
        return
    if len(sys.argv) != 3 or sys.argv[1] not in ("base", "cards"):
        sys.exit("usage: suite.py base|cards REPO_DIR, or suite.py sites")
    repo = os.path.abspath(sys.argv[2])
    (cmd_base if sys.argv[1] == "base" else cmd_cards)(repo, repos)


if __name__ == "__main__":
    main()
