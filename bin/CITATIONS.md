# Shared citation data

The canonical collector runs in `dongzhuoyao/acad-homepage` and publishes a
validated snapshot to its `google-scholar-stats` branch. This website imports
that branch's `citations.yml` into `_data/citations.yml`; it does not scrape
Google Scholar independently.

Source: https://raw.githubusercontent.com/dongzhuoyao/acad-homepage/google-scholar-stats/citations.yml

Publication badges match explicit `google_scholar_id` fields in
`_bibliography/papers.bib`. Copy the suffix after `EchdyZEAAAAJ:` from the paper's
Scholar URL when adding a paper. Missing matches are omitted, not shown as zero.
All authors in each bibliography entry are displayed without a collapsed list.
The site displays per-paper badges, with the source update date in their tooltip.
Aggregate citation totals are retained in the data but are not displayed.

Refresh locally from the repository root:

```sh
python3 -m pip install -r bin/requirements-citations.txt
python3 bin/update_scholar_citations.py
python3 -m unittest discover -s tests -v
```

The deployment workflow imports the shared snapshot on pushes, manual runs,
and daily at 16:47 Asia/Shanghai, after the collector's scheduled 16:00 run.
GitHub can delay scheduled jobs. Pull requests run importer tests and build
using the committed snapshot. The website does not require a cross-repository
secret to read these public statistics.

The importer validates the Scholar profile, every paper ID and count, the
publication count, summary metrics, and source timestamps before replacing data.
It preserves the collector's original update date. Older remote or cached
snapshots cannot overwrite newer data. If GitHub is unreachable or the snapshot
is invalid, the build retains the latest valid cache or committed snapshot.

The shared repository also continues to publish `gs_data.json` and
`gs_data_shieldsio.json` for existing clients and badges.
