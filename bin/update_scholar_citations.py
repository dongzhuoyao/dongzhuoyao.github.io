#!/usr/bin/env python3
"""Import the shared Google Scholar snapshot without scraping Scholar again."""

import argparse
from datetime import date, datetime, timezone
from pathlib import Path
import sys
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = 'https://raw.githubusercontent.com/dongzhuoyao/acad-homepage/google-scholar-stats/citations.yml'


def timestamp(data):
    value = datetime.fromisoformat(data['metadata']['fetched_at'])
    if value.tzinfo is None:
        raise ValueError('Snapshot timestamp must include its timezone.')
    return value.astimezone(timezone.utc)


def valid_snapshot(data, scholar_id):
    if not isinstance(data, dict):
        return False
    metadata, summary, papers = (data.get(key) for key in ('metadata', 'summary', 'papers'))
    if not all(isinstance(value, dict) for value in (metadata, summary, papers)):
        return False
    if metadata.get('scholar_user_id') != scholar_id or not papers:
        return False
    if type(metadata.get('publication_count')) is not int or metadata['publication_count'] != len(papers):
        return False
    if not isinstance(metadata.get('author_name'), str) or not metadata['author_name'].strip():
        return False
    for field in ('total_citations', 'h_index', 'i10_index'):
        count = summary.get(field)
        if type(count) is not int or count < 0:
            return False
    try:
        if date.fromisoformat(metadata['last_updated']) != timestamp(data).date():
            return False
    except (KeyError, TypeError, ValueError):
        return False
    for key, paper in papers.items():
        if not isinstance(key, str) or not key.startswith(scholar_id + ':') or not key.split(':', 1)[1]:
            return False
        if not isinstance(paper, dict) or not isinstance(paper.get('title'), str) or not paper['title'].strip():
            return False
        count = paper.get('citations')
        if type(count) is not int or count < 0:
            return False
    return True


def fetch_citations(scholar_id, fetch=None):
    if fetch is None:
        def fetch(url):
            request = Request(url, headers={'User-Agent': 'TaoHu-CitationSync/1.0'})
            with urlopen(request, timeout=20) as response:
                return response.read()
    data = yaml.safe_load(fetch(SOURCE_URL))
    if not valid_snapshot(data, scholar_id):
        raise ValueError('Shared citation snapshot is incomplete or belongs to a different profile.')
    return data


def read_snapshot(path, scholar_id):
    if path is None or not path.exists():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding='utf-8'))
        return data if valid_snapshot(data, scholar_id) else None
    except (OSError, yaml.YAMLError):
        return None


def write_snapshot(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding='utf-8')
    temporary.replace(path)


def update(scholar_id, output, cache=None, fetch=None):
    current = read_snapshot(output, scholar_id)
    cached = read_snapshot(cache, scholar_id)
    if cached and (current is None or timestamp(cached) > timestamp(current)):
        write_snapshot(output, cached)
        current = cached
    data = fetch_citations(scholar_id, fetch=fetch)
    # A stale CDN response must not overwrite a more recent saved snapshot.
    if current is not None and timestamp(current) > timestamp(data):
        data = current
    write_snapshot(output, data)
    if cache:
        write_snapshot(cache, data)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, help='Optional persistent cache for scheduled builds')
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / '_data/socials.yml').read_text())
    try:
        data = update(config['scholar_userid'], ROOT / '_data/citations.yml', args.cache)
    except Exception as error:
        print(f'Citation import failed; retained the previous snapshot: {error}', file=sys.stderr)
        return 1
    print(f"Imported {len(data['papers'])} papers for {data['metadata']['author_name']}: "
          f"{data['summary']['total_citations']} citations, updated {data['metadata']['last_updated']}.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
