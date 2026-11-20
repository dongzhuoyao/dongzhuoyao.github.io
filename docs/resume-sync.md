# Keep the website and résumé consistent

When an agent works on taohu.me, it should carry suitable verified facts into
Tao's Overleaf résumé during the same task. Tao authorized routine edits and
synchronization on 2026-11-20. Follow any narrower instruction in the current
request, including review-only or no-push limits.

## Decide what belongs in the résumé

Add or correct a fact when it is professionally relevant, supported by a source
inspected during the task or an explicit statement from Tao, and absent or
outdated in the résumé. Treat website text as evidence with provenance, not as
permission to strengthen a claim. Resolve conflicting sources before changing
the disputed detail.

| Fact | Usual résumé destination | Keep these distinctions |
| --- | --- | --- |
| Award or reviewer recognition | `0_awards.tex` | Exact title and year; no inferred rank or selection rate |
| Appointment or affiliation | `0_employment.tex` | Role, institution, dates, and part-time status |
| Degree | `0_education.tex` | Awarded versus expected; confirmed institution and date |
| Publication or acceptance | Relevant `.bib` file and `0_publication.tex` | Preprint versus accepted/published; exact authorship and venue |
| Academic service | `0_reviewer_experiences.tex`, `0_workshop_proposals.tex`, or the existing relevant section | Reviewer versus chair or organizer; workshop versus main conference |
| Teaching or supervision | `0_ta.tex` or `0_supervisions.tex` | Instructor versus teaching assistant; current versus incoming students |
| Grant, invited talk, or other substantial milestone | Existing relevant section, such as `0_talks.tex` | Confirmed role, status, and dates; disclose amounts only when intended for the CV |

Inspect the current résumé before choosing a destination; these paths describe
the current layout, not a permanent schema. Do not copy general research
interests, recruitment announcements, social posts, routine progress reports,
or speculative plans just because they appear in news. Avoid a second entry
when a publication changes from preprint to accepted: update the existing record
and any affected counters instead.

For example, the news entry `shared/news/eccv26_excellent_reviewer.md` supports
“ECCV 2026 · Excellent Reviewer” on the homepage and “ECCV Excellent Reviewer”
under 2026 in the English résumé. The Chinese version uses
“ECCV 优秀审稿人（Excellent Reviewer）”. The news publication date does not
establish the date of an award ceremony.

## Find the current sources

The homepage recognition list is in `_data/academic_service.yml`; news is authored in
`shared/news/`, profile text in `_pages/about.md`, and publications in
`shared/publications.bib`. After editing shared news or publications, run
`ruby scripts/sync_shared_content.rb` and include the generated copies for both
sites. Do not edit `_news/` or `_bibliography/papers.bib` directly.
Inspect the active layout before editing other CV-like files. In particular,
`assets/json/resume.json` contains theme demonstration data and is not the
authoritative résumé. The Overleaf LaTeX project is the résumé source.

Store the connection only in the git-ignored `.resume-sync.local.json`:

```json
{
  "checkout": "<absolute path to the local Overleaf checkout>",
  "remote": "origin",
  "branch": "main",
  "entrypoint": "main.tex"
}
```

Use existing local Git credentials. If the file is absent, resolve the résumé
repository from the user's saved context; if that is unavailable, ask for the
connection. Never guess among unrelated projects or put private connection
details in the public repository.

## Apply and verify the update

1. Inspect the website diff and identify the facts relevant to the current task.
   Verify wording, dates, and status. Check both résumé language branches for
   duplicates or an older form of each fact.
2. Read the résumé's project instructions and use `overleaf-pull` to fetch its
   current upstream. Preserve unrelated edits. When appropriate, use a separate
   worktree based on the fetched branch rather than changing a dirty checkout.
3. Make the smallest update in both language branches. Preserve the selected
   template, sections, existing facts, and default language. Do not rewrite the
   entire résumé or publish a CV PDF on the website as an incidental step.
4. Check the diff, compile both language variants in separate temporary build
   directories, and inspect the affected PDF pages. Check any changed citation
   records with the installed Overleaf source checker. For website data, parse
   the edited data, run `ruby scripts/sync_shared_content.rb --check` and
   `scripts/build_all.sh`, and inspect the deployment. Report unavailable local
   dependencies separately from CI results.
5. Commit only intended files. Use `overleaf-push` to synchronize the résumé to
   its configured branch, explicitly targeting that branch from a worktree.
   Publish website changes within the current task's authorization. Never
   force-push to resolve a collision.
6. Report both outcomes separately. Include the relevant commit IDs and the
   actual verification performed. If one side fails, retain the completed work
   and state which facts and files remain pending; do not claim both are synced.

This workflow runs when an agent handles a website task. GitHub Actions do not
make résumé judgments or access Overleaf, and no periodic job is implied.
