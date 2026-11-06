# The D-Modem sites

Each repository has a site at `https://d-modem.github.io/<repo>/`, and the
suite has one at <https://d-modem.github.io/> (the
[D-Modem.github.io](https://github.com/D-Modem/D-Modem.github.io)
repository). They are built with [Zensical](https://zensical.org/), the successor to
Material for MkDocs by the same team, and they all share what lives here:

| Path | What it is |
| --- | --- |
| `pages/mkdocs-base.yml` | The shared settings: the theme, light and dark schemes, Markdown extensions, search (in `mkdocs.yml`'s format, which Zensical reads) |
| `pages/theme/` | The theme's overrides: the suite's bar across the top, the Rainbow Book accent, the mark as logo and favicon |
| `pages/requirements.txt` | The pinned Zensical version |
| `tools/site.sh` | Puts the above into a repository and builds or previews its site |
| `pages/site_docs.py` | The site's copy of `docs/` for `docs_dir: .site/docs` |
| `.github/workflows/site.yml` | The reusable workflow that builds every site and deploys it to Pages |

A change here reaches every site on its next build.

## A repository's site

A repository needs three things: `mkdocs.yml`, its pages under `docs/`, and
`.github/workflows/pages.yml`.

`mkdocs.yml` inherits the shared settings and names the repository, whose
Rainbow Book becomes the site's accent ([palette.md](palette.md)):

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
builds the site, so a broken link fails it, and a push to main deploys it:

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

The workflow's inputs:

| Input | Default | What it does |
| --- | --- | --- |
| `prepare` | none | Shell commands run first, in the repository's root: the generators that write or check the reference pages |
| `go-version` | none | A Go version to install first, for generators written in Go |
| `submodules` | `false` | Passed to `actions/checkout` |
| `brand-ref` | `main` | The brand branch or tag whose theme to use |

A site whose pages are `docs/` plus the README can set `docs_dir: .site/docs`:
`tools/site.sh` then builds from a copy of `docs/` (`pages/site_docs.py`)
whose home page is the README and whose links that leave `docs/` (to
`../LICENSE`, to source files) go to the files on GitHub, so the same
Markdown reads right on GitHub and on the site. Images from outside
`docs/` (a README's banner, renders beside a page) come from GitHub's raw
files.

Pages that live elsewhere in the repository join the site when
`extra.site_include` lists them, as globs from the root; each keeps its
own path, and links between them stay on the site:

```yaml
extra:
  repo: hardware
  site_include:
    - SPEC*.md
    - firmware/*.md
```

`.site/` and `site/` go in the repository's `.gitignore`: the first is the
theme copied in for the build, the second the built site.

The repository's Pages source must be **GitHub Actions** (Settings → Pages →
Build and deployment → Source).

## Previewing

With a clone of brand beside the repository:

```sh
pip install -r ../brand/pages/requirements.txt
../brand/tools/site.sh . serve     # http://127.0.0.1:8000/
../brand/tools/site.sh . build     # what CI runs, into site/
```

Run the repository's generators first if it has any (its `prepare` line).

## Pages and generated reference

Each site has a landing page (`docs/index.md`) and a reference section that
lists every configurable option. The reference pages are written by a
generator in the repository from the code itself (an option table, a config
struct, a settings class), so they can't fall behind it. Generated pages are
built in CI rather than committed, and a generator fails when an option has
no description, so an undocumented option fails the build.
