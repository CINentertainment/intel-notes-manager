import sqlite3
from datetime import datetime


DATABASE_NAME = "intel_notes.db"


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

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


# --------------------------------------------------
# VALIDATION HELPERS
# --------------------------------------------------

def get_required_input(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be blank.")


def get_valid_date(prompt, allow_blank=False, current_value=None):
    while True:
        value = input(prompt).strip()

        if not value:
            if allow_blank:
                return current_value
            print("Date cannot be blank.")
            continue

        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, for example 2026-09-15.")


def get_classification(current_value=None):
    options = {
        "1": "UNCLASSIFIED",
        "2": "CUI",
        "3": "CONFIDENTIAL",
        "4": "SECRET",
        "5": "TOP SECRET"
    }

    while True:
        print("\nClassification:")
        print("1. UNCLASSIFIED")
        print("2. CUI")
        print("3. CONFIDENTIAL")
        print("4. SECRET")
        print("5. TOP SECRET")

        if current_value is not None:
            choice = input(
                f"Select classification [{current_value}] "
                "(Enter to keep current): "
            ).strip()

            if not choice:
                return current_value
        else:
            choice = input("Select classification (1-5): ").strip()

        if choice in options:
            return options[choice]

        print("Invalid selection. Please enter 1 through 5.")


def get_discipline(current_value=None):
    options = {
        "1": "HUMINT",
        "2": "SIGINT",
        "3": "GEOINT",
        "4": "OSINT",
        "5": "MASINT",
        "6": "ALL-SOURCE"
    }

    while True:
        print("\nINT Discipline:")
        print("1. HUMINT")
        print("2. SIGINT")
        print("3. GEOINT")
        print("4. OSINT")
        print("5. MASINT")
        print("6. ALL-SOURCE")

        if current_value is not None:
            choice = input(
                f"Select INT discipline [{current_value}] "
                "(Enter to keep current): "
            ).strip()

            if not choice:
                return current_value
        else:
            choice = input("Select INT discipline (1-6): ").strip()

        if choice in options:
            return options[choice]

        print("Invalid selection. Please enter 1 through 6.")


def get_reliability(current_value=None):
    descriptions = {
        "A": "Completely Reliable",
        "B": "Usually Reliable",
        "C": "Fairly Reliable",
        "D": "Not Usually Reliable",
        "E": "Unreliable",
        "F": "Reliability Cannot Be Judged"
    }

    while True:
        print("\nSource Reliability:")
        for code, description in descriptions.items():
            print(f"{code} - {description}")

        if current_value is not None:
            value = input(
                f"Source reliability [{current_value}] "
                "(Enter to keep current): "
            ).strip().upper()

            if not value:
                return current_value
        else:
            value = input("Source reliability (A-F): ").strip().upper()

        if value in descriptions:
            return value

        print("Invalid reliability rating. Please enter A through F.")


def get_credibility(current_value=None):
    descriptions = {
        "1": "Confirmed by Other Sources",
        "2": "Probably True",
        "3": "Possibly True",
        "4": "Doubtful",
        "5": "Improbable",
        "6": "Truth Cannot Be Judged"
    }

    while True:
        print("\nInformation Credibility:")
        for code, description in descriptions.items():
            print(f"{code} - {description}")

        if current_value is not None:
            value = input(
                f"Information credibility [{current_value}] "
                "(Enter to keep current): "
            ).strip()

            if not value:
                return current_value
        else:
            value = input("Information credibility (1-6): ").strip()

        if value in descriptions:
            return value

        print("Invalid credibility rating. Please enter 1 through 6.")


def reliability_description(code):
    descriptions = {
        "A": "Completely Reliable",
        "B": "Usually Reliable",
        "C": "Fairly Reliable",
        "D": "Not Usually Reliable",
        "E": "Unreliable",
        "F": "Reliability Cannot Be Judged"
    }

    return descriptions.get(code, "Unknown")


def credibility_description(code):
    descriptions = {
        "1": "Confirmed by Other Sources",
        "2": "Probably True",
        "3": "Possibly True",
        "4": "Doubtful",
        "5": "Improbable",
        "6": "Truth Cannot Be Judged"
    }

    return descriptions.get(code, "Unknown")


# --------------------------------------------------
# MENU
# --------------------------------------------------

def display_menu():
    print("\n" + "=" * 60)
    print("INTEL NOTES MANAGER")
    print("=" * 60)
    print("1. Create Intelligence Note")
    print("2. View Intelligence Notes")
    print("3. Search Intelligence Notes")
    print("4. Edit Intelligence Note")
    print("5. Delete Intelligence Note")
    print("6. Exit")
    print("=" * 60)


# --------------------------------------------------
# CREATE
# --------------------------------------------------

def create_note():
    print("\n" + "=" * 60)
    print("CREATE INTELLIGENCE NOTE")
    print("=" * 60)

    title = get_required_input("Title: ")
    date = get_valid_date("Date (YYYY-MM-DD): ")

    source = input("Source: ").strip()

    classification = get_classification()
    discipline = get_discipline()

    location = input("Location: ").strip()
    tags = input("Tags: ").strip()

    reliability = get_reliability()
    credibility = get_credibility()

    print("\nEnter intelligence note:")
    body = get_required_input("> ")

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

    note_id = cursor.lastrowid

    connection.close()

    print("\nIntelligence note saved successfully.")
    print(f"Assigned Note ID: {note_id}")


# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

def display_note(note):
    print("\n" + "-" * 60)
    print(f"NOTE ID: {note[0]}")
    print("-" * 60)

    print(f"Title: {note[1]}")
    print(f"Date: {note[2]}")
    print(f"Source: {note[3]}")
    print(f"Classification: {note[4]}")
    print(f"INT Discipline: {note[5]}")
    print(f"Location: {note[6]}")
    print(f"Tags: {note[7]}")

    print(
        f"Source Reliability: "
        f"{note[8]} - {reliability_description(note[8])}"
    )

    print(
        f"Information Credibility: "
        f"{note[9]} - {credibility_description(note[9])}"
    )

    print("-" * 60)
    print("Intelligence Note:")
    print(note[10])
    print("-" * 60)


# --------------------------------------------------
# RETRIEVE NOTE
# --------------------------------------------------

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


# --------------------------------------------------
# VIEW
# --------------------------------------------------

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

    if not notes:
        print("\nNo intelligence notes found.")
        return

    print("\n" + "=" * 60)
    print("INTELLIGENCE NOTES")
    print("=" * 60)

    for note in notes:
        display_note(note)

    print(f"\nTotal notes: {len(notes)}")


# --------------------------------------------------
# SEARCH
# --------------------------------------------------

def search_notes():
    print("\n" + "=" * 60)
    print("SEARCH INTELLIGENCE NOTES")
    print("=" * 60)

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

    if not results:
        print(f"\nNo notes found matching '{search_term}'.")
        return

    print(f"\nFound {len(results)} matching note(s).")

    for note in results:
        display_note(note)


# --------------------------------------------------
# EDIT
# --------------------------------------------------

def edit_note():
    print("\n" + "=" * 60)
    print("EDIT INTELLIGENCE NOTE")
    print("=" * 60)

    try:
        note_id = int(input("Enter Note ID to edit: ").strip())
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

    if not title:
        title = note[1]

    date = get_valid_date(
        f"Date [{note[2]}] (YYYY-MM-DD): ",
        allow_blank=True,
        current_value=note[2]
    )

    source = input(f"Source [{note[3]}]: ").strip()

    if not source:
        source = note[3]

    classification = get_classification(note[4])
    discipline = get_discipline(note[5])

    location = input(f"Location [{note[6]}]: ").strip()

    if not location:
        location = note[6]

    tags = input(f"Tags [{note[7]}]: ").strip()

    if not tags:
        tags = note[7]

    reliability = get_reliability(note[8])
    credibility = get_credibility(note[9])

    body = input(f"Note [{note[10]}]: ").strip()

    if not body:
        body = note[10]

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
        body,
        note_id
    ))

    connection.commit()
    connection.close()

    print("\nIntelligence note updated successfully.")


# --------------------------------------------------
# DELETE
# --------------------------------------------------

def delete_note():
    print("\n" + "=" * 60)
    print("DELETE INTELLIGENCE NOTE")
    print("=" * 60)

    try:
        note_id = int(input("Enter Note ID to delete: ").strip())
    except ValueError:
        print("\nInvalid Note ID.")
        return

    note = get_note_by_id(note_id)

    if note is None:
        print("\nNo note found with that ID.")
        return

    print("\nNote selected for deletion:")
    display_note(note)

    confirmation = input(
        "\nDelete this note? Type YES to confirm: "
    ).strip().upper()

    if confirmation != "YES":
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


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    create_database()

    print("=" * 60)
    print("INTEL NOTES MANAGER")
    print("=" * 60)
    print("Intelligence Note Management System")
    print("Database initialized successfully.")

    while True:
        display_menu()

        choice = input("Select an option: ").strip()

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