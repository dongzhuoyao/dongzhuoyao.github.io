# Managing taohu.me and taohu.me/lab

This repository owns both websites and deploys them as one GitHub Pages artifact.
The personal website remains at the repository root. The VIBE Lab website lives
in `lab/` and is built with `/lab` as its base URL.

## Shared content

Edit shared content only in these locations:

- `shared/publications.bib` — the publication source for both sites.
- `shared/news/` — the news source for both sites.

After an edit, synchronize the generated Jekyll inputs:

```bash
ruby scripts/sync_shared_content.rb
```

The deploy workflow checks that both generated copies match the shared source.
It will stop before deployment if someone edits `_bibliography/papers.bib` or
either `_news/` directory directly.

Personal biography, experience, and service content stays in the root site.
Lab members, recruiting information, and research areas stay under `lab/`.

## Local validation

Build both sites without Docker:

```bash
scripts/build_all.sh
```

Build and preview both sites from one local server:

```bash
scripts/preview_all.sh
```

The preview URLs are `http://127.0.0.1:4000/` and
`http://127.0.0.1:4000/lab/`.

## Deployment

The root `.github/workflows/deploy.yml` workflow builds both sites. It publishes
the personal site at the artifact root and the lab site in `_site/lab/`. The
nested workflow under `lab/.github/` is retained only as repository history and
does not run from this monorepo.
