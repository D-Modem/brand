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
case $what in
prepare) ;;
build) zensical build --strict ;;
serve) zensical serve ;;
*) echo "tools/site.sh: $what: build, serve or prepare" >&2; exit 2 ;;
esac
