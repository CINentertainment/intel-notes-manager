import os
import sqlite3
import unittest
from unittest.mock import patch

import database
import reporting


TEST_DATABASE = "test_reporting.db"
TEST_REPORTS_DIRECTORY = "test_reports"


class TestReporting(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        database.create_database(TEST_DATABASE)

        self.connection_patcher = patch(
            "database.get_connection",
            side_effect=lambda: sqlite3.connect(TEST_DATABASE)
        )
        self.connection_patcher.start()

        self.reports_directory_patcher = patch(
            "reporting.REPORTS_DIRECTORY",
            TEST_REPORTS_DIRECTORY
        )
        self.reports_directory_patcher.start()

        if os.path.exists(TEST_REPORTS_DIRECTORY):
            for filename in os.listdir(TEST_REPORTS_DIRECTORY):
                filepath = os.path.join(
                    TEST_REPORTS_DIRECTORY,
                    filename
                )

                if os.path.isfile(filepath):
                    os.remove(filepath)

            os.rmdir(TEST_REPORTS_DIRECTORY)

        self.insert_test_data()

    def tearDown(self):
        self.connection_patcher.stop()
        self.reports_directory_patcher.stop()

        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        if os.path.exists(TEST_REPORTS_DIRECTORY):
            for filename in os.listdir(TEST_REPORTS_DIRECTORY):
                filepath = os.path.join(
                    TEST_REPORTS_DIRECTORY,
                    filename
                )

                if os.path.isfile(filepath):
                    os.remove(filepath)

            os.rmdir(TEST_REPORTS_DIRECTORY)

    def insert_test_data(self):
        connection = sqlite3.connect(TEST_DATABASE)
        cursor = connection.cursor()

        test_notes = [
            (
                "Fictional HUMINT Report",
                "2026-09-10",
                "Source Alpha",
                "UNCLASSIFIED",
                "HUMINT",
                "San Antonio",
                "training, exercise",
                "B",
                "2",
                "Fictional HUMINT reporting."
            ),
            (
                "Fictional GEOINT Report",
                "2026-09-15",
                "Source Bravo",
                "SECRET",
                "GEOINT",
                "Taipei",
                "imagery, training",
                "A",
                "1",
                "Fictional GEOINT reporting."
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

    def test_create_reports_directory(self):
        reporting.create_reports_directory()

        self.assertTrue(
            os.path.isdir(TEST_REPORTS_DIRECTORY)
        )

    def test_format_distribution(self):
        results = [
            ("HUMINT", 2),
            ("GEOINT", 1)
        ]

        lines = reporting.format_distribution(
            "TEST DISTRIBUTION",
            results
        )

        self.assertIn(
            "TEST DISTRIBUTION",
            lines
        )

        self.assertIn(
            "HUMINT: 2",
            lines
        )

        self.assertIn(
            "GEOINT: 1",
            lines
        )

    def test_format_distribution_handles_empty_data(self):
        lines = reporting.format_distribution(
            "EMPTY TEST",
            []
        )

        self.assertIn(
            "No data available.",
            lines
        )

    def test_build_analytics_report(self):
        report = reporting.build_analytics_report()

        self.assertIn(
            "INTELLIGENCE ANALYTICS REPORT",
            report
        )

        self.assertIn(
            "Total Intelligence Notes: 2",
            report
        )

        self.assertIn(
            "HUMINT: 1",
            report
        )

        self.assertIn(
            "GEOINT: 1",
            report
        )

        self.assertIn(
            "A1: 1",
            report
        )

        self.assertIn(
            "B2: 1",
            report
        )

        self.assertIn(
            "training: 2",
            report
        )

        self.assertIn(
            "2026-09: 2",
            report
        )

    def test_generate_report_filename(self):
        filename = reporting.generate_report_filename()

        self.assertTrue(
            filename.startswith(
                "intelligence_analytics_"
            )
        )

        self.assertTrue(
            filename.endswith(".txt")
        )

    def test_export_analytics_report_creates_file(self):
        filepath = reporting.export_analytics_report()

        self.assertTrue(
            os.path.isfile(filepath)
        )

    def test_exported_report_contains_analytics(self):
        filepath = reporting.export_analytics_report()

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as report_file:
            contents = report_file.read()

        self.assertIn(
            "INTELLIGENCE ANALYTICS REPORT",
            contents
        )

        self.assertIn(
            "Total Intelligence Notes: 2",
            contents
        )

        self.assertIn(
            "SOURCE EVALUATION PAIRS",
            contents
        )

        self.assertIn(
            "REPORTING OVER TIME",
            contents
        )


if __name__ == "__main__":
    unittest.main()