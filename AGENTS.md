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

## Keep the Overleaf résumé current

Tao has authorized the following workflow: whenever work on this repository
adds, corrects, or discovers a verified fact suitable for his academic résumé,
also update the corresponding Overleaf résumé entry and synchronize it to
Overleaf. Do not ask for approval again for a routine update within this scope.
An explicit local-only, review-only, or no-push instruction takes precedence.

Follow [the résumé synchronization guide](docs/resume-sync.md). Assess the facts
encountered in the current task; a styling change does not require a full CV
audit. Suitable facts include honors, appointments, degrees, publications,
grants, academic service, teaching, and confirmed supervision milestones.
Preserve the distinction between planned and completed work.

Update both Chinese and English versions, keep the existing résumé structure,
and check for an existing entry before adding one. Never invent an award rank,
date, publication status, affiliation, or contribution. Ask about a material
ambiguity while continuing independent verified updates.

The connection is stored in the ignored `.resume-sync.local.json`, or can be
resolved from the user's saved résumé repository. Do not commit private
Overleaf URLs, credentials, or local absolute paths. Use the installed
`overleaf-pull` and `overleaf-push` workflows and preserve unrelated local work.

Report the website and résumé outcomes separately, including validation and
any unresolved synchronization failure. This is an instruction for agents
working in this repository; it does not create a background job or schedule.
