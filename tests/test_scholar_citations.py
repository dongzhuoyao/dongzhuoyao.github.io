"""Network-free checks for the shared snapshot importer and fallback behavior."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

import yaml

spec = importlib.util.spec_from_file_location('collector', Path(__file__).resolve().parents[1] / 'bin/update_scholar_citations.py')
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
ID = 'EchdyZEAAAAJ'


def snapshot(count=12, fetched_at='2026-11-08T15:18:51+00:00'):
    return {
        'metadata': {'scholar_user_id': ID, 'author_name': 'Vincent Tao Hu', 'publication_count': 2,
                     'fetched_at': fetched_at, 'last_updated': fetched_at[:10]},
        'summary': {'total_citations': 1781, 'h_index': 18, 'i10_index': 25},
        'papers': {ID + ':paper': {'title': 'Paper title', 'year': '2026', 'citations': count},
                   ID + ':new': {'title': 'New paper', 'year': '2026', 'citations': 0}},
    }


def fetch(data):
    return lambda _: yaml.safe_dump(data)


def fail(_):
    raise OSError('network unavailable')


class CitationTests(unittest.TestCase):
    def test_shared_endpoint_preserves_counts_and_original_timestamp(self):
        expected = snapshot()
        urls = []
        def download(url):
            urls.append(url)
            return yaml.safe_dump(expected)
        data = collector.fetch_citations(ID, fetch=download)
        self.assertEqual(urls, [collector.SOURCE_URL])
        self.assertIn('/acad-homepage/google-scholar-stats/citations.yml', urls[0])
        self.assertEqual(data, expected)
        self.assertEqual(data['papers'][ID + ':new']['citations'], 0)

    def test_wrong_profile_and_foreign_paper_rejected(self):
        wrong = snapshot()
        wrong['metadata']['scholar_user_id'] = 'Einstein'
        foreign = snapshot()
        foreign['papers']['Einstein:paper'] = foreign['papers'].pop(ID + ':paper')
        for data in (wrong, foreign):
            with self.subTest(data=data), self.assertRaises(ValueError):
                collector.fetch_citations(ID, fetch=fetch(data))

    def test_partial_or_malformed_snapshot_rejected(self):
        invalid = [None, [], {}, {'metadata': None}, '<html>Access denied</html>']
        for field in ('summary', 'papers', 'metadata'):
            data = snapshot()
            data.pop(field)
            invalid.append(data)
        partial = snapshot()
        partial['papers'].pop(ID + ':new')
        invalid.append(partial)
        for data in invalid:
            with self.subTest(data=data), self.assertRaises(ValueError):
                collector.fetch_citations(ID, fetch=fetch(data))

    def test_invalid_counts_rejected(self):
        for value in (-1, True, None, '12'):
            for target in ('paper', 'total'):
                data = snapshot()
                if target == 'paper': data['papers'][ID + ':paper']['citations'] = value
                else: data['summary']['total_citations'] = value
                with self.subTest(value=value, target=target):
                    self.assertFalse(collector.valid_snapshot(data, ID))

    def test_invalid_timestamps_rejected(self):
        for value in ('unknown', '2026-11-08T12:00:00', None):
            data = snapshot()
            data['metadata']['fetched_at'] = value
            self.assertFalse(collector.valid_snapshot(data, ID))
        data = snapshot()
        data['metadata']['last_updated'] = '2026-11-07'
        self.assertFalse(collector.valid_snapshot(data, ID))

    def test_failed_or_invalid_import_preserves_file(self):
        for download in (fail, fetch({})):
            with self.subTest(download=download), tempfile.TemporaryDirectory() as directory:
                out = Path(directory) / 'citations.yml'
                collector.write_snapshot(out, snapshot())
                original = out.read_bytes()
                with self.assertRaises((OSError, ValueError)):
                    collector.update(ID, out, fetch=download)
                self.assertEqual(out.read_bytes(), original)

    def test_newer_cache_survives_failed_import(self):
        with tempfile.TemporaryDirectory() as directory:
            out, cache = Path(directory) / 'citations.yml', Path(directory) / 'cached.yml'
            collector.write_snapshot(out, snapshot(fetched_at='2026-11-07T15:00:00+00:00'))
            newer = snapshot(count=15)
            collector.write_snapshot(cache, newer)
            with self.assertRaises(OSError): collector.update(ID, out, cache, fetch=fail)
            self.assertEqual(yaml.safe_load(out.read_text()), newer)

    def test_foreign_or_malformed_cache_ignored(self):
        foreign = snapshot()
        foreign['metadata']['scholar_user_id'] = 'Einstein'
        for bad in (foreign, {'metadata': []}, 'bad yaml: ['):
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as directory:
                out, cache = Path(directory) / 'citations.yml', Path(directory) / 'cached.yml'
                expected = snapshot()
                collector.write_snapshot(out, expected)
                cache.write_text(bad if isinstance(bad, str) else yaml.safe_dump(bad))
                with self.assertRaises(OSError): collector.update(ID, out, cache, fetch=fail)
                self.assertEqual(yaml.safe_load(out.read_text()), expected)

    def test_older_upstream_and_cache_do_not_downgrade(self):
        with tempfile.TemporaryDirectory() as directory:
            out, cache = Path(directory) / 'citations.yml', Path(directory) / 'cached.yml'
            newer = snapshot(count=15)
            old = snapshot(fetched_at='2026-11-07T15:00:00+00:00')
            collector.write_snapshot(out, newer)
            collector.write_snapshot(cache, old)
            self.assertEqual(collector.update(ID, out, cache, fetch=fetch(old)), newer)
            self.assertEqual(yaml.safe_load(cache.read_text()), newer)

    def test_successful_import_updates_output_and_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            out, cache = Path(directory) / 'citations.yml', Path(directory) / 'cached.yml'
            expected = snapshot()
            collector.update(ID, out, cache, fetch=fetch(expected))
            self.assertEqual(yaml.safe_load(out.read_text()), expected)
            self.assertEqual(yaml.safe_load(cache.read_text()), expected)


if __name__ == '__main__':
    unittest.main()
