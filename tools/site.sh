#!/bin/sh
# A D-Modem repository's site, built the way its Pages workflow builds it.
#
#   tools/site.sh REPO_DIR [build|serve|prepare]
#
# prepare puts the shared theme and settings in REPO_DIR/.site/ (the repo's
# mkdocs.yml starts with "INHERIT: .site/mkdocs-base.yml"); build then runs
# zensical build --strict into REPO_DIR/site/, serve a live preview on
# http://127.0.0.1:8000/. Needs pages/requirements.txt installed
# (pip install -r pages/requirements.txt).
set -eu
brand=$(cd "$(dirname "$0")/.." && pwd)
repo=${1:?usage: tools/site.sh REPO_DIR [build|serve|prepare]}
what=${2:-build}
cd "$repo"
rm -rf .site/theme
mkdir -p .site
cp -R "$brand/pages/theme" .site/theme
cp "$brand/pages/mkdocs-base.yml" .site/mkdocs-base.yml
cp "$brand/avatar/mark.svg" .site/theme/assets/suite/mark.svg
# the core repositories of the suite (pages/suite.yml): the bar, the accent
python3 "$brand/pages/suite.py" base .
# a site built from a copy of docs/ (docs_dir: .site/docs): the copy, its
# home page the README and its links out of docs/ to GitHub
if grep -q '^docs_dir: *\.site/docs' mkdocs.yml 2>/dev/null; then
	python3 "$brand/pages/site_docs.py" .
	# "<!-- suite:cards -->": the cards of the suite's core repositories
	python3 "$brand/pages/suite.py" cards .
elif grep -rqs '<!-- *suite:cards *-->' docs; then
	echo "tools/site.sh: a page has <!-- suite:cards -->, thus mkdocs.yml must have docs_dir: .site/docs" >&2
	exit 1
fi
case $what in
prepare) ;;
build) zensical build --strict ;;
serve) zensical serve ;;
*) echo "tools/site.sh: $what: build, serve or prepare" >&2; exit 2 ;;
esac
