# AGENTS.md

Guidance for Codex when working with this repository.

## Rules
- Avoid changing upstream theme templates unless necessary; stay aligned with the al-folio upstream.
- Keep site content focused on the HUST research AI lab: Generative Models, Robotics, Large Vision Models, and Brain-Computer Interface. Recruiting emphasis: PhD and Masters; Bachelors welcome for research participation.
- Preserve existing patterns and structure; prefer incremental edits over large rewrites.

## Project Overview
Research lab website built with Jekyll using the [al-folio](https://github.com/alshedivat/al-folio) theme, hosted on GitHub Pages at `dongzhuoyao.github.io/lab`. The lab is VIBE at HUST, China. The site highlights a basic intro of the PI, the team, and current open opportunities.

## Tech Stack
- Static site generator: Jekyll
- Theme: al-folio
- Templating: Liquid
- Styling: SCSS/Bootstrap
- Hosting: GitHub Pages

## Directory Structure
- `_pages/` — Main site pages (about, publications, projects, team, etc.)
- `_posts/` — Blog posts
- `_projects/` — Project entries
- `_news/` — News/announcement items
- `_layouts/` — Page templates (Liquid)
- `_includes/` — Reusable components
- `_data/` — YAML data files (coauthors, cv, venues)
- `_sass/` — SCSS stylesheets
- `_bibliography/` — BibTeX files for publications
- `assets/` — Static files (images, CSS, JS)

## Key Files
- `_config.yml` — Main Jekyll configuration
- `_pages/about.md` — Homepage
- `_bibliography/papers.bib` — Publication bibliography

## Navigation
Pages appear in the navbar when they have `nav: true` in their front matter. Order is controlled by `nav_order`.

```yaml
---
layout: page
title: page title
permalink: /url/
nav: true
nav_order: 4
---
```

## Common Tasks
- **Add a new page:** create a `.md` in `_pages/`, set layout/title/permalink, add `nav: true` and `nav_order` to include in navigation.
- **Add a publication:** add a BibTeX entry to `_bibliography/papers.bib`; optional preview image in `assets/img/publication_preview/`.
- **Add a team member:** update the appropriate data file or page; add profile image to `assets/img/`.

## Running Locally
```bash
bundle install
bundle exec jekyll serve
```

## Docker Build
```bash
docker compose up
```

## Style Guidelines
- Keep pages simple and focused; reuse Bootstrap components and existing patterns.
- Store images in `assets/img/`.
- Favor clarity and brevity in copy; avoid unnecessary flourish.
