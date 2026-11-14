# The D-Modem sites

Each repository has a site at `https://d-modem.github.io/<repo>/`. The
suite has a site at <https://d-modem.github.io/> (the
[D-Modem.github.io](https://github.com/D-Modem/D-Modem.github.io)
repository). The sites are built with [Zensical](https://zensical.org/). Zensical is the successor to
Material for MkDocs, from the same team. All the sites share the files in this repository:

| Path | What it is |
| --- | --- |
| `pages/mkdocs-base.yml` | The shared settings: the theme, light and dark schemes, Markdown extensions, search (in the format of `mkdocs.yml`, which Zensical reads) |
| `pages/theme/` | The overrides of the theme: the bar of the suite across the top, the Rainbow Book accent, the mark as logo and favicon |
| `pages/requirements.txt` | The pinned Zensical version |
| `tools/site.sh` | Puts the items above into a repository, and builds or previews its site |
| `pages/site_docs.py` | The copy of `docs/` for the site, for `docs_dir: .site/docs` |
| `.github/workflows/site.yml` | The reusable workflow that builds each site and deploys it to Pages |

A change here goes to each site on its next build.

## A repository's site

A repository needs three items: `mkdocs.yml`, its pages under `docs/`, and
`.github/workflows/pages.yml`.

`mkdocs.yml` inherits the shared settings and names the repository. The
Rainbow Book of the repository becomes the accent of the site
([palette.md](palette.md)):

```yaml
INHERIT: .site/mkdocs-base.yml
site_name: D-Modem bbs
site_url: https://d-modem.github.io/bbs/
repo_url: https://github.com/D-Modem/bbs
repo_name: D-Modem/bbs
extra:
  repo: bbs
nav:
  - Home: index.md
  - ...
```

`.github/workflows/pages.yml` calls the shared workflow. A pull request
builds the site, thus a broken link causes the pull request to fail. A push
to main deploys the site:

```yaml
name: Pages
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages-${{ github.ref }}
  cancel-in-progress: true
jobs:
  site:
    uses: D-Modem/brand/.github/workflows/site.yml@main
```

The inputs of the workflow:

| Input | Default | What it does |
| --- | --- | --- |
| `prepare` | none | Shell commands that run first, in the root of the repository: the generators that write or check the reference pages |
| `go-version` | none | A Go version to install first, for generators written in Go |
| `submodules` | `false` | Passed to `actions/checkout` |
| `brand-ref` | `main` | The brand branch or tag that has the theme to use |

If the pages of a site are `docs/` and the README, the site can set
`docs_dir: .site/docs`. Then `tools/site.sh` builds from a copy of `docs/`
(`pages/site_docs.py`). In this copy, the README is the home page. The links
that go out of `docs/` (to `../LICENSE`, to source files) go to the files on
GitHub. Thus the same Markdown shows correctly on GitHub and on the site.
Images from outside `docs/` (the banner of a README, renders next to a page)
come from the raw files of GitHub.

Pages in other locations of the repository become part of the site if
`extra.site_include` lists them, as globs from the root. Each page keeps its
own path, and links between them stay on the site:

```yaml
extra:
  repo: hardware
  site_include:
    - SPEC*.md
    - firmware/*.md
```

Put `.site/` and `site/` in the `.gitignore` of the repository. `.site/` is
the theme that the build copies in. `site/` is the built site.

The Pages source of the repository must be **GitHub Actions** (Settings → Pages →
Build and deployment → Source).

## Preview

Put a clone of brand next to the repository. Then use these commands:

```sh
pip install -r ../brand/pages/requirements.txt
../brand/tools/site.sh . serve     # http://127.0.0.1:8000/
../brand/tools/site.sh . build     # what CI runs, into site/
```

If the repository has generators, run them first (its `prepare` line).

## Pages and generated reference

Each site has a landing page (`docs/index.md`) and a reference section that
lists each configurable option. A generator in the repository writes the
reference pages from the code (an option table, a config struct, a settings
class). Thus the pages always agree with the code. CI builds the generated
pages, and they are not committed. A generator fails if an option has no
description. Thus an option without a description causes the build to fail.
