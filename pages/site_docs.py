#!/usr/bin/env python3
# The site's copy of a repository's docs/, for sites whose mkdocs.yml says
# docs_dir: .site/docs (tools/site.sh runs this when it does):
#
#   - docs/ is copied to .site/docs/, so nothing in docs/ changes;
#   - the home page, .site/docs/index.md, is the repository's README.md
#     (unless docs/ has an index.md of its own);
#   - pages from elsewhere in the repository that extra.site_include in
#     mkdocs.yml lists (globs from the root, such as SPEC*.md or
#     firmware/README.md) are copied too, at their own paths;
#   - an image from outside docs/ (a README's banner, a render beside a
#     page) comes from GitHub, its raw file;
#   - a link that leaves docs/ (../LICENSE, ../src/x.go, a README link to
#     a file beside it) goes to the file on GitHub instead, as repo_url
#     in mkdocs.yml names it, unless it is to one of those pages.
#
#   python3 site_docs.py REPO_DIR
import glob
import os
import re
import shutil
import sys

LINK_RE = re.compile(r"(\]\()([^)\s]+)(\))")
IMG_RE = re.compile(r"(!\[[^\]]*\]\()([^)\s]+)(\))")
SRC_RE = re.compile(r"(<img\b[^>]*?\bsrc=\")([^\"]+)(\")")


def config(repo):
    with open(os.path.join(repo, "mkdocs.yml"), encoding="utf-8") as f:
        return f.read()


def repo_url(text):
    m = re.search(r"^repo_url:\s*(\S+)", text, re.M)
    if not m:
        sys.exit("site_docs: mkdocs.yml has no repo_url")
    return m.group(1).rstrip("/")


def includes(repo, text):
    """The pages extra.site_include lists, as paths from the root."""
    m = re.search(r"^  site_include:\s*\n((?:    - .*\n?)+)", text, re.M)
    pats = re.findall(r"^    - +[\"']?([^\"'\n]+?)[\"']?\s*$", m.group(1), re.M) if m else []
    found = set()
    for pat in pats:
        hits = glob.glob(os.path.join(repo, pat), recursive=True)
        if not hits:
            sys.exit("site_docs: extra.site_include: %s matches nothing" % pat)
        for h in hits:
            rel = os.path.relpath(h, repo).replace(os.sep, "/")
            if rel.endswith(".md") and not rel.startswith("docs/"):
                found.add(rel)
    return found


def site_path(whole, extra):
    """Where the repository's file `whole` is in the site, or None."""
    if whole.startswith("docs/"):
        return whole[len("docs/"):]
    if whole == "README.md":
        return "index.md"
    if whole in extra:
        return whole
    return None


def site_image(target, page, raw):
    """An image of the page `page`: one outside docs/ comes from GitHub."""
    if re.match(r"[a-z][a-z0-9+.-]*:|#|/", target):
        return target
    whole = os.path.normpath(os.path.join(os.path.dirname(page), target)).replace(os.sep, "/")
    if whole.startswith("docs/") and page.startswith("docs/"):
        return target
    return raw + whole


def site_link(target, page, extra, blob):
    """A link of the page `page` (its path from the root) as the site has it."""
    if re.match(r"[a-z][a-z0-9+.-]*:|#", target):
        return target
    path, _, frag = target.partition("#")
    if not path:
        return target
    here = os.path.dirname(page)
    whole = os.path.normpath(os.path.join(here, path)).replace(os.sep, "/")
    if whole == "docs" or (whole.startswith("docs/") and page.startswith("docs/")):
        return target
    dest = site_path(whole, extra)
    if dest is None:
        new = blob + whole
    else:
        new = os.path.relpath(dest, os.path.dirname(site_path(page, extra))).replace(os.sep, "/")
    return new + ("#" + frag if frag else "")


def rewrite(text, page, extra, blob):
    raw = blob.replace("/blob/", "/raw/", 1)
    image = lambda m: m.group(1) + site_image(m.group(2), page, raw) + m.group(3)
    text = SRC_RE.sub(image, IMG_RE.sub(image, text))
    return LINK_RE.sub(lambda m: m.group(1) + site_link(m.group(2), page, extra, blob) + m.group(3), text)


def main():
    repo = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    text = config(repo)
    blob = repo_url(text) + "/blob/main/"
    extra = includes(repo, text)
    src = os.path.join(repo, "docs")
    dst = os.path.join(repo, ".site", "docs")
    shutil.rmtree(dst, ignore_errors=True)
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        os.makedirs(dst)
    pages = []
    for d, _, files in os.walk(dst):
        for f in files:
            if f.endswith(".md"):
                pages.append("docs/" + os.path.relpath(os.path.join(d, f), dst).replace(os.sep, "/"))
    index = os.path.join(dst, "index.md")
    if not os.path.exists(index) and os.path.exists(os.path.join(repo, "README.md")):
        pages.append("README.md")
    pages += sorted(extra)
    for page in pages:
        with open(os.path.join(repo, page), encoding="utf-8") as fh:
            text = fh.read()
        out = os.path.join(dst, site_path(page, extra))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(rewrite(text, page, extra, blob))


if __name__ == "__main__":
    main()
