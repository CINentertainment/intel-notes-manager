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
    print("4. Edit Intelligence Note")
    print("5. Delete Intelligence Note")
    print("6. Exit")
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


def get_note_by_id(note_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM notes
        WHERE id = ?
    """, (note_id,))

    note = cursor.fetchone()

    connection.close()

    return note


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


def edit_note():
    print("\n" + "=" * 50)
    print("EDIT INTELLIGENCE NOTE")
    print("=" * 50)

    try:
        note_id = int(input("Enter Note ID to edit: "))
    except ValueError:
        print("\nInvalid Note ID.")
        return

    note = get_note_by_id(note_id)

    if note is None:
        print("\nNo note found with that ID.")
        return

    print("\nCurrent note:")
    display_note(note)

    print("\nPress Enter to keep the current value.")

    title = input(f"Title [{note[1]}]: ").strip()
    date = input(f"Date [{note[2]}]: ").strip()
    source = input(f"Source [{note[3]}]: ").strip()
    classification = input(f"Classification [{note[4]}]: ").strip()
    discipline = input(f"INT Discipline [{note[5]}]: ").strip()
    location = input(f"Location [{note[6]}]: ").strip()
    tags = input(f"Tags [{note[7]}]: ").strip()
    reliability = input(f"Source Reliability [{note[8]}]: ").strip()
    credibility = input(f"Information Credibility [{note[9]}]: ").strip()
    body = input(f"Note [{note[10]}]: ").strip()

    updated_values = (
        title if title else note[1],
        date if date else note[2],
        source if source else note[3],
        classification if classification else note[4],
        discipline if discipline else note[5],
        location if location else note[6],
        tags if tags else note[7],
        reliability if reliability else note[8],
        credibility if credibility else note[9],
        body if body else note[10],
        note_id
    )

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE notes
        SET title = ?,
            date = ?,
            source = ?,
            classification = ?,
            discipline = ?,
            location = ?,
            tags = ?,
            reliability = ?,
            credibility = ?,
            body = ?
        WHERE id = ?
    """, updated_values)

    connection.commit()
    connection.close()

    print("\nIntelligence note updated successfully.")


def delete_note():
    print("\n" + "=" * 50)
    print("DELETE INTELLIGENCE NOTE")
    print("=" * 50)

    try:
        note_id = int(input("Enter Note ID to delete: "))
    except ValueError:
        print("\nInvalid Note ID.")
        return

    note = get_note_by_id(note_id)

    if note is None:
        print("\nNo note found with that ID.")
        return

    print("\nNote selected for deletion:")
    display_note(note)

    confirmation = input("\nDelete this note? (y/n): ").strip().lower()

    if confirmation != "y":
        print("\nDeletion cancelled.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM notes
        WHERE id = ?
    """, (note_id,))

    connection.commit()
    connection.close()

    print("\nIntelligence note deleted successfully.")


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
            edit_note()

        elif choice == "5":
            delete_note()

        elif choice == "6":
            print("\nExiting Intel Notes Manager.")
            break

        else:
            print("\nInvalid selection. Please enter 1 through 6.")


if __name__ == "__main__":
    main()