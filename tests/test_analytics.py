import os
import sqlite3
import unittest
from unittest.mock import patch

import analytics
import database


TEST_DATABASE = "test_analytics.db"


class TestAnalytics(unittest.TestCase):

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
                "Fictional HUMINT Report One",
                "2026-09-01",
                "Source Alpha",
                "UNCLASSIFIED",
                "HUMINT",
                "Mexico City",
                "training, border",
                "B",
                "2",
                "Fictional HUMINT reporting."
            ),
            (
                "Fictional HUMINT Report Two",
                "2026-09-05",
                "Source Bravo",
                "CUI",
                "HUMINT",
                "San Antonio",
                "training, exercise",
                "B",
                "2",
                "Additional fictional HUMINT reporting."
            ),
            (
                "Fictional GEOINT Report",
                "2026-09-10",
                "Source Charlie",
                "SECRET",
                "GEOINT",
                "Taipei",
                "imagery, training",
                "A",
                "1",
                "Fictional GEOINT reporting."
            ),
            (
                "Fictional OSINT Report",
                "2026-09-20",
                "Source Delta",
                "UNCLASSIFIED",
                "OSINT",
                "San Antonio",
                "cyber, training",
                "C",
                "3",
                "Fictional OSINT reporting."
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

    def test_get_total_notes(self):
        total = analytics.get_total_notes()

        self.assertEqual(total, 4)

    def test_get_discipline_distribution(self):
        results = analytics.get_discipline_distribution()

        distribution = dict(results)

        self.assertEqual(distribution["HUMINT"], 2)
        self.assertEqual(distribution["GEOINT"], 1)
        self.assertEqual(distribution["OSINT"], 1)

    def test_get_classification_distribution(self):
        results = analytics.get_classification_distribution()

        distribution = dict(results)

        self.assertEqual(distribution["UNCLASSIFIED"], 2)
        self.assertEqual(distribution["CUI"], 1)
        self.assertEqual(distribution["SECRET"], 1)

    def test_get_reliability_distribution(self):
        results = analytics.get_reliability_distribution()

        distribution = dict(results)

        self.assertEqual(distribution["A"], 1)
        self.assertEqual(distribution["B"], 2)
        self.assertEqual(distribution["C"], 1)

    def test_get_credibility_distribution(self):
        results = analytics.get_credibility_distribution()

        distribution = dict(results)

        self.assertEqual(distribution["1"], 1)
        self.assertEqual(distribution["2"], 2)
        self.assertEqual(distribution["3"], 1)

    def test_get_location_distribution(self):
        results = analytics.get_location_distribution()

        distribution = dict(results)

        self.assertEqual(distribution["San Antonio"], 2)
        self.assertEqual(distribution["Mexico City"], 1)
        self.assertEqual(distribution["Taipei"], 1)

    def test_location_distribution_orders_by_count(self):
        results = analytics.get_location_distribution()

        self.assertEqual(
            results[0],
            ("San Antonio", 2)
        )

    @patch("builtins.print")
    def test_display_analytics(self, mock_print):
        analytics.display_analytics()

        printed_output = " ".join(
            str(call)
            for call in mock_print.call_args_list
        )

        self.assertIn(
            "INTELLIGENCE ANALYTICS",
            printed_output
        )

        self.assertIn(
            "Total Intelligence Notes: 4",
            printed_output
        )

        self.assertIn(
            "INT DISCIPLINE DISTRIBUTION",
            printed_output
        )

        self.assertIn(
            "CLASSIFICATION DISTRIBUTION",
            printed_output
        )

        self.assertIn(
            "TOP LOCATIONS",
            printed_output
        )

    def test_empty_database_returns_zero_notes(self):
        connection = sqlite3.connect(TEST_DATABASE)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM notes")

        connection.commit()
        connection.close()

        total = analytics.get_total_notes()

        self.assertEqual(total, 0)


if __name__ == "__main__":
    unittest.main()