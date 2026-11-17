# Unified website guidance

This repository publishes two Jekyll sites in one GitHub Pages artifact:

- The repository root builds `https://taohu.me/`.
- `lab/` builds `https://taohu.me/lab/`.

## Shared sources

- Edit publications in `shared/publications.bib`.
- Edit news in `shared/news/`.
- Run `ruby scripts/sync_shared_content.rb` after changing either source.
- Do not edit the generated `_bibliography/papers.bib` or `_news/` copies directly.

## Validation

- Run `ruby scripts/sync_shared_content.rb --check`.
- Run `scripts/build_all.sh` to build both sites without Docker.
- Preserve the separate navigation, layouts, and visual identities of the personal and lab sites.
- Keep lab-only members, recruiting information, and research areas under `lab/`.
- Prefer incremental theme changes and follow the additional instructions in `lab/AGENTS.md` when editing the lab site.
