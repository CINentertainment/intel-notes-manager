import os
import sqlite3
import unittest

from database import create_database


TEST_DATABASE = "test_intel_notes.db"


class TestDatabase(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        create_database(TEST_DATABASE)

    def tearDown(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

    def test_database_file_is_created(self):
        self.assertTrue(os.path.exists(TEST_DATABASE))

    def test_notes_table_is_created(self):
        connection = sqlite3.connect(TEST_DATABASE)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'notes'
        """)

        table = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(table)
        self.assertEqual(table[0], "notes")

    def test_notes_table_has_expected_columns(self):
        connection = sqlite3.connect(TEST_DATABASE)
        cursor = connection.cursor()

        cursor.execute("PRAGMA table_info(notes)")

        columns = cursor.fetchall()

        connection.close()

        column_names = [
            column[1]
            for column in columns
        ]

        expected_columns = [
            "id",
            "title",
            "date",
            "source",
            "classification",
            "discipline",
            "location",
            "tags",
            "reliability",
            "credibility",
            "body"
        ]

        self.assertEqual(
            column_names,
            expected_columns
        )

    def test_note_can_be_inserted(self):
        connection = sqlite3.connect(TEST_DATABASE)
        cursor = connection.cursor()

        cursor.execute("""
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
        """, (
            "Fictional HUMINT Report",
            "2026-09-18",
            "Test Source",
            "UNCLASSIFIED",
            "HUMINT",
            "Fictional Location",
            "test, training",
            "B",
            "2",
            "This is fictional test data."
        ))

        connection.commit()

        cursor.execute("""
            SELECT *
            FROM notes
            WHERE title = ?
        """, ("Fictional HUMINT Report",))

        note = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(note)
        self.assertEqual(
            note[1],
            "Fictional HUMINT Report"
        )
        self.assertEqual(note[4], "UNCLASSIFIED")
        self.assertEqual(note[5], "HUMINT")
        self.assertEqual(note[8], "B")
        self.assertEqual(note[9], "2")


if __name__ == "__main__":
    unittest.main()