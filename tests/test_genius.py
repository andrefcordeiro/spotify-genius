import unittest

from spotify_genius.core.genius import (
    build_search_queries,
    remove_features,
    select_best_candidate,
    strip_version_tags,
)


class GeniusMatchingTests(unittest.TestCase):
    def test_remove_features_handles_parentheses_and_brackets(self):
        self.assertEqual(remove_features("Song Title (feat. Artist)"), "Song Title")
        self.assertEqual(remove_features("Song Title [ft. Artist]"), "Song Title")

    def test_strip_version_tags_removes_release_suffixes(self):
        self.assertEqual(strip_version_tags("Song Title - Remastered 2012"), "Song Title")
        self.assertEqual(strip_version_tags("Song Title (Live at Wembley)"), "Song Title")

    def test_build_search_queries_keeps_symbol_only_titles(self):
        queries = build_search_queries("Bring Me The Horizon", "¿")
        self.assertIn("Bring Me The Horizon ¿", queries)
        self.assertIn("¿ Bring Me The Horizon", queries)

    def test_select_best_candidate_prefers_exact_unicode_match(self):
        hits = [
            {
                "result": {
                    "title": "mother tongue",
                    "title_with_featured": "mother tongue",
                    "primary_artist": {"name": "Bring Me The Horizon"},
                    "url": "https://genius.com/Bring-me-the-horizon-mother-tongue-lyrics",
                }
            },
            {
                "result": {
                    "title": "¿",
                    "title_with_featured": "¿",
                    "primary_artist": {"name": "Bring Me The Horizon"},
                    "url": "https://genius.com/Bring-me-the-horizon-lyrics",
                }
            },
        ]

        candidate = select_best_candidate("Bring Me The Horizon", "¿", hits)

        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.url, "https://genius.com/Bring-me-the-horizon-lyrics")

    def test_select_best_candidate_rejects_low_confidence_matches(self):
        hits = [
            {
                "result": {
                    "title": "Medicine",
                    "title_with_featured": "Medicine",
                    "primary_artist": {"name": "Daughter"},
                    "url": "https://genius.com/Bring-me-the-horizon-medicine-lyrics",
                }
            },
            {
                "result": {
                    "title": "Parasite Eve",
                    "title_with_featured": "Parasite Eve",
                    "primary_artist": {"name": "Bring Me The Horizon"},
                    "url": "https://genius.com/Bring-me-the-horizon-parasite-eve-lyrics",
                }
            },
        ]

        candidate = select_best_candidate("Bring Me The Horizon", "Medicine", hits)

        self.assertIsNone(candidate)


if __name__ == "__main__":
    unittest.main()
