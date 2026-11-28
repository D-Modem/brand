# The D-Modem sites

Each repository has a site at `https://d-modem.github.io/<repo>/`. The
suite has a site at <https://d-modem.github.io/> (the
[D-Modem.github.io](https://github.com/D-Modem/D-Modem.github.io)
repository). The sites are built with [Zensical](https://zensical.org/). Zensical is the successor to
Material for MkDocs, from the same team. All the sites share the files in this repository:

| Path | What it is |
| --- | --- |
| `pages/mkdocs-base.yml` | The shared settings: the theme, light and dark schemes, Markdown extensions, search (in the format of `mkdocs.yml`, which Zensical reads) |
| `pages/suite.yml` | The list of the core repositories of the suite: the bar across the top of each site, the accent of each site, and the cards on the home page |
| `pages/suite.py` | Puts the list of `pages/suite.yml` into a site |
| `pages/theme/` | The overrides of the theme: the bar of the suite across the top, the Rainbow Book accent, the mark as logo and favicon |
| `pages/requirements.txt` | The pinned Zensical version |
| `tools/site.sh` | Puts the items above into a repository, and builds or previews its site |
| `pages/site_docs.py` | The copy of `docs/` for the site, for `docs_dir: .site/docs` |
| `.github/workflows/site.yml` | The reusable workflow that builds each site and deploys it to Pages |
| `.github/workflows/sites.yml` | Builds each site again when one of the items above changes on main |

When one of these items changes on main, the Sites workflow
(`.github/workflows/sites.yml`) builds each site again. Refer to
[The core repositories](#the-core-repositories).

## The core repositories

`pages/suite.yml` is the list of the core repositories of the suite. It is
the only location of this data. The list gives:

- The links in the bar across the top of each site, in the order of the list.
- The accent colour of each site.
- The cards in "The suite" on <https://d-modem.github.io/>. A page that has
  the line `<!-- suite:cards -->` gets the cards in place of this line.

Put only the core repositories in the list. A repository that is not in the
list can have a site, but the bar and the home page do not show it. A
support library, for example go3270, is not a core repository. Its site
has the carrier green as its accent.

Each entry has these keys:

| Key | What it is |
| --- | --- |
| `name` | The name of the repository. Its site is `https://d-modem.github.io/<name>/`. |
| `title` | The text that the bar shows when the pointer is on the name |
| `colour` | The Book colour of the repository, as `#rrggbb`. It must be the same as in `REPOS` of `tools/gen.py`. |
| `card` | The text of the card on the home page, in Markdown |

When the list or the theme changes on main, the Sites workflow starts the
Pages workflow of each site that uses the list: each core repository
(but brand, which builds its own site), and D-Modem.github.io. Each site
then has the new bar and the new cards. You do not change the other
repositories.

The Sites workflow uses the organization secret `DMODEM_BUMP_TOKEN`. The
token must have **Actions: read and write** on each of those repositories,
and brand must have access to the secret. If the token cannot start the
workflow of a repository, the job of that repository fails. The other jobs
continue.

### Add a core repository

1. Make the site of the new repository. Refer to
   [A repository's site](#a-repositorys-site).
2. Give the repository a Book: add it to `REPOS` in `tools/gen.py`.
3. Add an entry for the repository to `pages/suite.yml`. Use the same
   colour as in `tools/gen.py`.
4. Run `python3 tools/brand_ref.py`. This updates `docs/reference.md` and
   checks the colours.
5. Add the repository to the fine-grained token of the
   `DMODEM_BUMP_TOKEN` secret, with **Actions: read and write**.
6. Merge the pull request. The Sites workflow builds each site again.

To remove a core repository:

1. Remove its entry from `pages/suite.yml`.
2. Remove it from `REPOS` in `tools/gen.py`, and remove its rules from
   `pages/theme/assets/suite/d-modem.css`. Its Book is then free.
3. Run `python3 tools/brand_ref.py`.
4. Remove its row from the suite table of each README
   ([readme-template.md](readme-template.md)).
5. Merge the pull request. The Sites workflow builds each site again.
   The Sites workflow does not build the site of the removed repository.
   Start the Pages workflow of that repository manually, so that its bar
   does not show it.

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

If a page of the site has the line `<!-- suite:cards -->`, the site must
set `docs_dir: .site/docs`. The build then changes the copy, not the page
in `docs/`.

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
