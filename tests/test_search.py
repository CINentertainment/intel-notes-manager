import os
import sqlite3
import unittest
from unittest.mock import patch

import database
import search


TEST_DATABASE = "test_search.db"


class TestSearch(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        database.create_database(TEST_DATABASE)

        self.connection_patcher = patch(
            "database.get_connection",
            side_effect=lambda: sqlite3.connect(TEST_DATABASE)
        )

        self.connection_patcher.start()

        self.insert_test_data()

    def tearDown(self):
        self.connection_patcher.stop()

        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

    def insert_test_data(self):
        connection = sqlite3.connect(TEST_DATABASE)
        cursor = connection.cursor()

        test_notes = [
            (
                "Fictional HUMINT Report",
                "2026-09-01",
                "Source Alpha",
                "UNCLASSIFIED",
                "HUMINT",
                "Mexico City",
                "training, border",
                "B",
                "2",
                "Fictional HUMINT reporting for testing."
            ),
            (
                "Fictional GEOINT Report",
                "2026-09-10",
                "Source Bravo",
                "SECRET",
                "GEOINT",
                "Taipei",
                "imagery, training",
                "A",
                "1",
                "Fictional GEOINT reporting for testing."
            ),
            (
                "Fictional OSINT Report",
                "2026-09-20",
                "Source Charlie",
                "CUI",
                "OSINT",
                "San Antonio",
                "cyber, training",
                "C",
                "3",
                "Fictional OSINT reporting for testing."
            )
        ]

        cursor.executemany("""
            INSERT INTO notes (
                title,
                date,
                source,
                classification,
                discipline,
                location,
                tags,
                reliability,
                credibility,
                body
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, test_notes)

        connection.commit()
        connection.close()

    def capture_results(self, function, user_input):
        with patch(
            "builtins.input",
            side_effect=user_input
        ):
            with patch(
                "search.display_results"
            ) as mock_display:

                function()

                mock_display.assert_called_once()

                return mock_display.call_args[0][0]

    def test_keyword_search(self):
        results = self.capture_results(
            search.keyword_search,
            ["GEOINT"]
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0][1],
            "Fictional GEOINT Report"
        )

    def test_filter_by_classification(self):
        results = self.capture_results(
            search.filter_by_classification,
            ["4"]
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0][4],
            "SECRET"
        )

    def test_filter_by_discipline(self):
        results = self.capture_results(
            search.filter_by_discipline,
            ["1"]
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0][5],
            "HUMINT"
        )

    def test_filter_by_reliability(self):
        results = self.capture_results(
            search.filter_by_reliability,
            ["A"]
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0][8],
            "A"
        )

    def test_filter_by_credibility(self):
        results = self.capture_results(
            search.filter_by_credibility,
            ["3"]
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0][9],
            "3"
        )

    def test_filter_by_date_range(self):
        results = self.capture_results(
            search.filter_by_date_range,
            [
                "2026-09-05",
                "2026-09-15"
            ]
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0][1],
            "Fictional GEOINT Report"
        )

    def test_filter_by_location(self):
        results = self.capture_results(
            search.filter_by_location,
            ["San Antonio"]
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0][5],
            "OSINT"
        )

    def test_combined_filter(self):
        results = self.capture_results(
            search.combined_filter,
            [
                "1",    # UNCLASSIFIED
                "1",    # HUMINT
                "B",    # Reliability
                "2",    # Credibility
                "",     # Location
                "",     # Tag / keyword
                "",     # Start date
                ""      # End date
            ]
        )

        self.assertEqual(len(results), 1)

        note = results[0]

        self.assertEqual(
            note[1],
            "Fictional HUMINT Report"
        )
        self.assertEqual(
            note[4],
            "UNCLASSIFIED"
        )
        self.assertEqual(
            note[5],
            "HUMINT"
        )
        self.assertEqual(
            note[8],
            "B"
        )
        self.assertEqual(
            note[9],
            "2"
        )

    def test_combined_filter_returns_no_matches(self):
        results = self.capture_results(
            search.combined_filter,
            [
                "5",    # TOP SECRET
                "0",    # ANY discipline
                "0",    # ANY reliability
                "0",    # ANY credibility
                "",     # Location
                "",     # Tag / keyword
                "",     # Start date
                ""      # End date
            ]
        )

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()