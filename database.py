import sqlite3


DATABASE_NAME = "intel_notes.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT,
            source TEXT,
            classification TEXT,
            discipline TEXT,
            location TEXT,
            tags TEXT,
            reliability TEXT,
            credibility TEXT,
            body TEXT
        )
    """)

    connection.commit()
    connection.close()


def get_connection():
    return sqlite3.connect(DATABASE_NAME)