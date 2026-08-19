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


def display_menu():
    print("\n" + "=" * 50)
    print("INTEL NOTES MANAGER")
    print("=" * 50)
    print("1. Create Intelligence Note")
    print("2. View Intelligence Notes")
    print("3. Search Intelligence Notes")
    print("4. Exit")
    print("=" * 50)


def create_note():
    print("\n" + "=" * 50)
    print("CREATE INTELLIGENCE NOTE")
    print("=" * 50)

    title = input("Title: ")
    date = input("Date: ")
    source = input("Source: ")
    classification = input("Classification: ")
    discipline = input("INT Discipline: ")
    location = input("Location: ")
    tags = input("Tags: ")
    reliability = input("Source Reliability (A-F): ")
    credibility = input("Information Credibility (1-6): ")

    print("\nEnter intelligence note:")
    body = input("> ")

    connection = sqlite3.connect(DATABASE_NAME)
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
    ))

    connection.commit()
    connection.close()

    print("\nIntelligence note saved successfully.")


def display_note(note):
    print(f"\nNote ID: {note[0]}")
    print("-" * 50)
    print(f"Title: {note[1]}")
    print(f"Date: {note[2]}")
    print(f"Source: {note[3]}")
    print(f"Classification: {note[4]}")
    print(f"INT Discipline: {note[5]}")
    print(f"Location: {note[6]}")
    print(f"Tags: {note[7]}")
    print(f"Source Reliability: {note[8]}")
    print(f"Information Credibility: {note[9]}")
    print(f"Note: {note[10]}")


def view_notes():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM notes
        ORDER BY id
    """)

    notes = cursor.fetchall()

    connection.close()

    if len(notes) == 0:
        print("\nNo intelligence notes found.")
        return

    print("\n" + "=" * 50)
    print("INTELLIGENCE NOTES")
    print("=" * 50)

    for note in notes:
        display_note(note)

    print(f"\nTotal notes: {len(notes)}")


def search_notes():
    print("\n" + "=" * 50)
    print("SEARCH INTELLIGENCE NOTES")
    print("=" * 50)

    search_term = input("Enter search term: ").strip()

    if not search_term:
        print("\nSearch term cannot be empty.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    search_pattern = f"%{search_term}%"

    cursor.execute("""
        SELECT *
        FROM notes
        WHERE title LIKE ?
           OR date LIKE ?
           OR source LIKE ?
           OR classification LIKE ?
           OR discipline LIKE ?
           OR location LIKE ?
           OR tags LIKE ?
           OR reliability LIKE ?
           OR credibility LIKE ?
           OR body LIKE ?
        ORDER BY id
    """, (
        search_pattern,
        search_pattern,
        search_pattern,
        search_pattern,
        search_pattern,
        search_pattern,
        search_pattern,
        search_pattern,
        search_pattern,
        search_pattern
    ))

    results = cursor.fetchall()

    connection.close()

    if len(results) == 0:
        print(f"\nNo notes found matching '{search_term}'.")
        return

    print(f"\nFound {len(results)} matching note(s).")

    for note in results:
        display_note(note)


def main():
    create_database()

    print("=" * 50)
    print("INTEL NOTES MANAGER")
    print("=" * 50)
    print("Intelligence Note Management System")
    print("Database initialized successfully.")

    while True:
        display_menu()

        choice = input("Select an option: ")

        if choice == "1":
            create_note()

        elif choice == "2":
            view_notes()

        elif choice == "3":
            search_notes()

        elif choice == "4":
            print("\nExiting Intel Notes Manager.")
            break

        else:
            print("\nInvalid selection. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()