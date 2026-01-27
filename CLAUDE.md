# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.


# Rules

- Try to avoid changing the template files, and follow the upstream repo.
- Always respect the implementation of the upstream, so we can enjoy the feature design of them.
- This is a lab website - keep content focused on the research group.

## Project Overview

This is a research lab website built with Jekyll using the [al-folio](https://github.com/alshedivat/al-folio) theme. It is hosted on GitHub Pages at `dongzhuoyao.github.io/lab`.

## Tech Stack

- **Static Site Generator**: Jekyll
- **Theme**: al-folio (academic portfolio theme)
- **Templating**: Liquid
- **Styling**: SCSS/Bootstrap
- **Hosting**: GitHub Pages

## Directory Structure

- `_pages/` - Main site pages (about, publications, projects, team, etc.)
- `_posts/` - Blog posts
- `_projects/` - Project entries
- `_news/` - News/announcement items
- `_layouts/` - Page templates (Liquid)
- `_includes/` - Reusable components
- `_data/` - YAML data files (coauthors, cv, venues)
- `_sass/` - SCSS stylesheets
- `_bibliography/` - BibTeX files for publications
- `assets/` - Static files (images, CSS, JS)

## Key Files

- `_config.yml` - Main Jekyll configuration
- `_pages/about.md` - Homepage
- `_bibliography/papers.bib` - Publication bibliography

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

### Adding a new page
1. Create a `.md` file in `_pages/`
2. Add front matter with layout, title, permalink
3. Set `nav: true` and `nav_order` to include in navigation

### Adding a publication
1. Add BibTeX entry to `_bibliography/papers.bib`
2. Optionally add preview image to `assets/img/publication_preview/`

### Adding a team member
1. Add member info to the appropriate data file or page
2. Add profile image to `assets/img/`

### Running locally
```bash
bundle install
bundle exec jekyll serve
```

### Building with Docker
```bash
docker compose up
```

## Style Guidelines

- Keep pages simple and focused
- Use Bootstrap classes for styling (cards, grids, etc.)
- Images go in `assets/img/`
- Follow existing patterns in similar pages
