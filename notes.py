import database

from validation import (
    credibility_description,
    get_classification,
    get_credibility,
    get_discipline,
    get_reliability,
    get_required_input,
    get_valid_date,
    reliability_description
)


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
# RETRIEVE
# ============================================================

def get_note_by_id(note_id):
    connection = database.get_connection()
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

    connection = database.get_connection()
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
# VIEW
# ============================================================

def view_notes():
    connection = database.get_connection()
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

    connection = database.get_connection()
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

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM notes
        WHERE id = ?
    """, (note_id,))

    connection.commit()
    connection.close()

    print("\nIntelligence note deleted successfully.")