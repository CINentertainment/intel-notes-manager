import os
import sqlite3
import unittest
from unittest.mock import patch

import database
import notes


TEST_DATABASE = "test_notes.db"


class TestNotes(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

        database.create_database(TEST_DATABASE)

        self.connection_patcher = patch(
            "database.get_connection",
            side_effect=lambda: sqlite3.connect(TEST_DATABASE)
        )

        self.connection_patcher.start()

    def tearDown(self):
        self.connection_patcher.stop()

        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)

    def insert_test_note(self):
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
            "2026-09-21",
            "Test Source",
            "UNCLASSIFIED",
            "HUMINT",
            "Fictional Location",
            "training, test",
            "B",
            "2",
            "This is fictional test data."
        ))

        connection.commit()

        note_id = cursor.lastrowid

        connection.close()

        return note_id

    def test_get_note_by_id_returns_note(self):
        note_id = self.insert_test_note()

        note = notes.get_note_by_id(note_id)

        self.assertIsNotNone(note)
        self.assertEqual(note[0], note_id)
        self.assertEqual(note[1], "Fictional HUMINT Report")
        self.assertEqual(note[4], "UNCLASSIFIED")
        self.assertEqual(note[5], "HUMINT")
        self.assertEqual(note[8], "B")
        self.assertEqual(note[9], "2")

    def test_get_note_by_id_returns_none_for_missing_note(self):
        note = notes.get_note_by_id(999)

        self.assertIsNone(note)

    @patch("builtins.input")
    def test_create_note(self, mock_input):
        mock_input.side_effect = [
            "Automated Test Report",
            "2026-09-21",
            "Automated Test Source",
            "1",
            "1",
            "Test Location",
            "automated, unittest",
            "B",
            "2",
            "Created by an automated unit test."
        ]

        notes.create_note()

        connection = sqlite3.connect(TEST_DATABASE)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM notes
            WHERE title = ?
        """, ("Automated Test Report",))

        note = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(note)
        self.assertEqual(note[1], "Automated Test Report")
        self.assertEqual(note[4], "UNCLASSIFIED")
        self.assertEqual(note[5], "HUMINT")
        self.assertEqual(note[8], "B")
        self.assertEqual(note[9], "2")

    @patch("builtins.input")
    def test_edit_note(self, mock_input):
        note_id = self.insert_test_note()

        mock_input.side_effect = [
            str(note_id),
            "Updated Fictional Report",
            "",
            "",
            "",
            "",
            "Updated Location",
            "",
            "",
            "",
            "Updated fictional test data."
        ]

        notes.edit_note()

        updated_note = notes.get_note_by_id(note_id)

        self.assertIsNotNone(updated_note)
        self.assertEqual(
            updated_note[1],
            "Updated Fictional Report"
        )
        self.assertEqual(
            updated_note[6],
            "Updated Location"
        )
        self.assertEqual(
            updated_note[10],
            "Updated fictional test data."
        )

        self.assertEqual(
            updated_note[4],
            "UNCLASSIFIED"
        )
        self.assertEqual(
            updated_note[5],
            "HUMINT"
        )

    @patch("builtins.input")
    def test_delete_note(self, mock_input):
        note_id = self.insert_test_note()

        mock_input.side_effect = [
            str(note_id),
            "YES"
        ]

        notes.delete_note()

        deleted_note = notes.get_note_by_id(note_id)

        self.assertIsNone(deleted_note)

    @patch("builtins.input")
    def test_delete_note_can_be_cancelled(self, mock_input):
        note_id = self.insert_test_note()

        mock_input.side_effect = [
            str(note_id),
            "NO"
        ]

        notes.delete_note()

        existing_note = notes.get_note_by_id(note_id)

        self.assertIsNotNone(existing_note)


if __name__ == "__main__":
    unittest.main()