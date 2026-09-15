import sqlite3
from datetime import datetime


DATABASE_NAME = "intel_notes.db"


# ============================================================
# DATABASE
# ============================================================

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


# ============================================================
# VALIDATION
# ============================================================

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
            print(
                "Invalid date. Use YYYY-MM-DD, "
                "for example 2026-09-15."
            )


def get_classification(current_value=None, allow_any=False):
    options = {
        "1": "UNCLASSIFIED",
        "2": "CUI",
        "3": "CONFIDENTIAL",
        "4": "SECRET",
        "5": "TOP SECRET"
    }

    while True:
        print("\nClassification:")

        if allow_any:
            print("0. ANY")

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
            choice = input("Select classification: ").strip()

        if allow_any and choice == "0":
            return None

        if choice in options:
            return options[choice]

        print("Invalid classification selection.")


def get_discipline(current_value=None, allow_any=False):
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

        if allow_any:
            print("0. ANY")

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
            choice = input("Select INT discipline: ").strip()

        if allow_any and choice == "0":
            return None

        if choice in options:
            return options[choice]

        print("Invalid INT discipline selection.")


def get_reliability(current_value=None, allow_any=False):
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

        if allow_any:
            print("0 - ANY")

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
            value = input("Source reliability: ").strip().upper()

        if allow_any and value == "0":
            return None

        if value in descriptions:
            return value

        print("Invalid reliability rating.")


def get_credibility(current_value=None, allow_any=False):
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

        if allow_any:
            print("0 - ANY")

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
            value = input("Information credibility: ").strip()

        if allow_any and value == "0":
            return None

        if value in descriptions:
            return value

        print("Invalid credibility rating.")


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


# ============================================================
# DISPLAY
# ============================================================

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


def display_results(results):
    if not results:
        print("\nNo matching intelligence notes found.")
        return

    print(f"\nFound {len(results)} matching note(s).")

    for note in results:
        display_note(note)


# ============================================================
# CREATE
# ============================================================

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


# ============================================================
# RETRIEVE
# ============================================================

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


# ============================================================
# VIEW
# ============================================================

def view_notes():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM notes
        ORDER BY date DESC, id DESC
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


# ============================================================
# GENERAL KEYWORD SEARCH
# ============================================================

def keyword_search():
    print("\n" + "=" * 60)
    print("GENERAL KEYWORD SEARCH")
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
        ORDER BY date DESC, id DESC
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

    display_results(results)


# ============================================================
# CLASSIFICATION FILTER
# ============================================================

def filter_by_classification():
    print("\n" + "=" * 60)
    print("FILTER BY CLASSIFICATION")
    print("=" * 60)

    classification = get_classification()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM notes
        WHERE classification = ?
        ORDER BY date DESC, id DESC
    """, (classification,))

    results = cursor.fetchall()

    connection.close()

    display_results(results)


# ============================================================
# DISCIPLINE FILTER
# ============================================================

def filter_by_discipline():
    print("\n" + "=" * 60)
    print("FILTER BY INT DISCIPLINE")
    print("=" * 60)

    discipline = get_discipline()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM notes
        WHERE discipline = ?
        ORDER BY date DESC, id DESC
    """, (discipline,))

    results = cursor.fetchall()

    connection.close()

    display_results(results)


# ============================================================
# RELIABILITY FILTER
# ============================================================

def filter_by_reliability():
    print("\n" + "=" * 60)
    print("FILTER BY SOURCE RELIABILITY")
    print("=" * 60)

    reliability = get_reliability()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM notes
        WHERE reliability = ?
        ORDER BY date DESC, id DESC
    """, (reliability,))

    results = cursor.fetchall()

    connection.close()

    display_results(results)


# ============================================================
# CREDIBILITY FILTER
# ============================================================

def filter_by_credibility():
    print("\n" + "=" * 60)
    print("FILTER BY INFORMATION CREDIBILITY")
    print("=" * 60)

    credibility = get_credibility()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM notes
        WHERE credibility = ?
        ORDER BY date DESC, id DESC
    """, (credibility,))

    results = cursor.fetchall()

    connection.close()

    display_results(results)


# ============================================================
# DATE RANGE FILTER
# ============================================================

def filter_by_date_range():
    print("\n" + "=" * 60)
    print("FILTER BY DATE RANGE")
    print("=" * 60)

    start_date = get_valid_date(
        "Start date (YYYY-MM-DD): "
    )

    end_date = get_valid_date(
        "End date (YYYY-MM-DD): "
    )

    if start_date > end_date:
        print("\nStart date cannot be after end date.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM notes
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC, id DESC
    """, (
        start_date,
        end_date
    ))

    results = cursor.fetchall()

    connection.close()

    display_results(results)


# ============================================================
# LOCATION FILTER
# ============================================================

def filter_by_location():
    print("\n" + "=" * 60)
    print("FILTER BY LOCATION")
    print("=" * 60)

    location = input("Enter location: ").strip()

    if not location:
        print("\nLocation cannot be empty.")
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM notes
        WHERE location LIKE ?
        ORDER BY date DESC, id DESC
    """, (f"%{location}%",))

    results = cursor.fetchall()

    connection.close()

    display_results(results)


# ============================================================
# COMBINED INTELLIGENCE FILTER
# ============================================================

def combined_filter():
    print("\n" + "=" * 60)
    print("COMBINED INTELLIGENCE FILTER")
    print("=" * 60)

    print(
        "\nSelect filters to apply. "
        "Choose ANY where you do not want a restriction."
    )

    classification = get_classification(allow_any=True)
    discipline = get_discipline(allow_any=True)
    reliability = get_reliability(allow_any=True)
    credibility = get_credibility(allow_any=True)

    print("\nOptional additional filters.")
    print("Press Enter to skip a field.")

    location = input("Location: ").strip()
    tags = input("Tag or keyword: ").strip()

    start_date_input = input(
        "Start date YYYY-MM-DD (Enter to skip): "
    ).strip()

    end_date_input = input(
        "End date YYYY-MM-DD (Enter to skip): "
    ).strip()

    start_date = None
    end_date = None

    if start_date_input:
        try:
            start_date = datetime.strptime(
                start_date_input,
                "%Y-%m-%d"
            ).strftime("%Y-%m-%d")

        except ValueError:
            print("\nInvalid start date.")
            return

    if end_date_input:
        try:
            end_date = datetime.strptime(
                end_date_input,
                "%Y-%m-%d"
            ).strftime("%Y-%m-%d")

        except ValueError:
            print("\nInvalid end date.")
            return

    if start_date and end_date and start_date > end_date:
        print("\nStart date cannot be after end date.")
        return

    query = """
        SELECT *
        FROM notes
        WHERE 1 = 1
    """

    parameters = []

    if classification:
        query += " AND classification = ?"
        parameters.append(classification)

    if discipline:
        query += " AND discipline = ?"
        parameters.append(discipline)

    if reliability:
        query += " AND reliability = ?"
        parameters.append(reliability)

    if credibility:
        query += " AND credibility = ?"
        parameters.append(credibility)

    if location:
        query += " AND location LIKE ?"
        parameters.append(f"%{location}%")

    if tags:
        query += """
            AND (
                tags LIKE ?
                OR title LIKE ?
                OR body LIKE ?
            )
        """

        pattern = f"%{tags}%"

        parameters.extend([
            pattern,
            pattern,
            pattern
        ])

    if start_date:
        query += " AND date >= ?"
        parameters.append(start_date)

    if end_date:
        query += " AND date <= ?"
        parameters.append(end_date)

    query += " ORDER BY date DESC, id DESC"

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(query, parameters)

    results = cursor.fetchall()

    connection.close()

    print("\n" + "=" * 60)
    print("FILTER RESULTS")
    print("=" * 60)

    display_results(results)


# ============================================================
# SEARCH MENU
# ============================================================

def search_notes():
    while True:
        print("\n" + "=" * 60)
        print("SEARCH & FILTER INTELLIGENCE NOTES")
        print("=" * 60)

        print("1. General Keyword Search")
        print("2. Filter by Classification")
        print("3. Filter by INT Discipline")
        print("4. Filter by Source Reliability")
        print("5. Filter by Information Credibility")
        print("6. Filter by Date Range")
        print("7. Filter by Location")
        print("8. Combined Intelligence Filter")
        print("9. Return to Main Menu")

        print("=" * 60)

        choice = input("Select an option: ").strip()

        if choice == "1":
            keyword_search()

        elif choice == "2":
            filter_by_classification()

        elif choice == "3":
            filter_by_discipline()

        elif choice == "4":
            filter_by_reliability()

        elif choice == "5":
            filter_by_credibility()

        elif choice == "6":
            filter_by_date_range()

        elif choice == "7":
            filter_by_location()

        elif choice == "8":
            combined_filter()

        elif choice == "9":
            return

        else:
            print(
                "\nInvalid selection. "
                "Please enter 1 through 9."
            )


# ============================================================
# EDIT
# ============================================================

def edit_note():
    print("\n" + "=" * 60)
    print("EDIT INTELLIGENCE NOTE")
    print("=" * 60)

    try:
        note_id = int(
            input("Enter Note ID to edit: ").strip()
        )

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

    title = input(
        f"Title [{note[1]}]: "
    ).strip()

    if not title:
        title = note[1]

    date = get_valid_date(
        f"Date [{note[2]}] (YYYY-MM-DD): ",
        allow_blank=True,
        current_value=note[2]
    )

    source = input(
        f"Source [{note[3]}]: "
    ).strip()

    if not source:
        source = note[3]

    classification = get_classification(note[4])
    discipline = get_discipline(note[5])

    location = input(
        f"Location [{note[6]}]: "
    ).strip()

    if not location:
        location = note[6]

    tags = input(
        f"Tags [{note[7]}]: "
    ).strip()

    if not tags:
        tags = note[7]

    reliability = get_reliability(note[8])
    credibility = get_credibility(note[9])

    body = input(
        f"Note [{note[10]}]: "
    ).strip()

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


# ============================================================
# DELETE
# ============================================================

def delete_note():
    print("\n" + "=" * 60)
    print("DELETE INTELLIGENCE NOTE")
    print("=" * 60)

    try:
        note_id = int(
            input("Enter Note ID to delete: ").strip()
        )

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


# ============================================================
# MAIN MENU
# ============================================================

def display_menu():
    print("\n" + "=" * 60)
    print("INTEL NOTES MANAGER")
    print("=" * 60)

    print("1. Create Intelligence Note")
    print("2. View Intelligence Notes")
    print("3. Search & Filter Intelligence Notes")
    print("4. Edit Intelligence Note")
    print("5. Delete Intelligence Note")
    print("6. Exit")

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

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
            print(
                "\nInvalid selection. "
                "Please enter 1 through 6."
            )


if __name__ == "__main__":
    main()