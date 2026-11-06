#!/usr/bin/env python3
# The site's copy of a repository's docs/, for sites whose mkdocs.yml says
# docs_dir: .site/docs (tools/site.sh runs this when it does):
#
#   - docs/ is copied to .site/docs/, so nothing in docs/ changes;
#   - the home page, .site/docs/index.md, is the repository's README.md
#     (unless docs/ has an index.md of its own);
#   - a link that leaves docs/ (../LICENSE, ../src/x.go, a README link to
#     a file beside it) goes to the file on GitHub instead, as repo_url
#     in mkdocs.yml names it.
#
#   python3 site_docs.py REPO_DIR
import os
import re
import shutil
import sys

LINK_RE = re.compile(r"(\]\()([^)\s]+)(\))")


def repo_url(repo):
    with open(os.path.join(repo, "mkdocs.yml"), encoding="utf-8") as f:
        m = re.search(r"^repo_url:\s*(\S+)", f.read(), re.M)
    if not m:
        sys.exit("site_docs: mkdocs.yml has no repo_url")
    return m.group(1).rstrip("/")


def site_link(target, page_dir, blob):
    """A link of a page in docs/<page_dir> as the site has it."""
    if re.match(r"[a-z][a-z0-9+.-]*:|#", target):
        return target
    path, _, frag = target.partition("#")
    if not path:
        return target
    whole = os.path.normpath(os.path.join("docs", page_dir, path)).replace(os.sep, "/")
    if whole == "docs" or whole.startswith("docs/"):
        return target
    if whole == "README.md":
        new = os.path.relpath("docs/index.md", os.path.join("docs", page_dir))
    else:
        new = blob + whole
    return new + ("#" + frag if frag else "")


def rewrite(text, page_dir, blob):
    return LINK_RE.sub(lambda m: m.group(1) + site_link(m.group(2), page_dir, blob) + m.group(3), text)


def main():
    repo = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    blob = repo_url(repo) + "/blob/main/"
    src = os.path.join(repo, "docs")
    dst = os.path.join(repo, ".site", "docs")
    shutil.rmtree(dst, ignore_errors=True)
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        os.makedirs(dst)
    for d, _, files in os.walk(dst):
        page_dir = os.path.relpath(d, dst)
        page_dir = "" if page_dir == "." else page_dir
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(d, f)
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(rewrite(text, page_dir, blob))
    index = os.path.join(dst, "index.md")
    readme = os.path.join(repo, "README.md")
    if not os.path.exists(index) and os.path.exists(readme):
        with open(readme, encoding="utf-8") as fh:
            text = fh.read()

        # the README's links are from the repository's root
        def home_link(m):
            t = m.group(2)
            if re.match(r"[a-z][a-z0-9+.-]*:|#", t):
                return m.group(0)
            path, _, frag = t.partition("#")
            rel = os.path.relpath(path, "docs") if path else path
            return m.group(1) + site_link(rel + ("#" + frag if frag else ""), "", blob) + m.group(3)

        with open(index, "w", encoding="utf-8") as fh:
            fh.write(LINK_RE.sub(home_link, text))


if __name__ == "__main__":
    main()
