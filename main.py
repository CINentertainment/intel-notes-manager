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

    note = {
        "title": title,
        "date": date,
        "source": source,
        "classification": classification,
        "discipline": discipline,
        "location": location,
        "tags": tags,
        "reliability": reliability,
        "credibility": credibility,
        "body": body
    }

    print("\nIntelligence note created successfully.")

    return note


def display_note(note, number=None):
    if number is not None:
        print(f"\nNote #{number}")

    print("-" * 50)
    print(f"Title: {note['title']}")
    print(f"Date: {note['date']}")
    print(f"Source: {note['source']}")
    print(f"Classification: {note['classification']}")
    print(f"INT Discipline: {note['discipline']}")
    print(f"Location: {note['location']}")
    print(f"Tags: {note['tags']}")
    print(f"Source Reliability: {note['reliability']}")
    print(f"Information Credibility: {note['credibility']}")
    print(f"Note: {note['body']}")


def view_notes(notes):
    if len(notes) == 0:
        print("\nNo intelligence notes found.")
        return

    print("\n" + "=" * 50)
    print("INTELLIGENCE NOTES")
    print("=" * 50)

    for index, note in enumerate(notes, start=1):
        display_note(note, index)


def search_notes(notes):
    if len(notes) == 0:
        print("\nNo intelligence notes available to search.")
        return

    print("\n" + "=" * 50)
    print("SEARCH INTELLIGENCE NOTES")
    print("=" * 50)

    search_term = input("Enter search term: ").strip().lower()

    results = []

    for note in notes:
        searchable_text = " ".join([
            note["title"],
            note["date"],
            note["source"],
            note["classification"],
            note["discipline"],
            note["location"],
            note["tags"],
            note["reliability"],
            note["credibility"],
            note["body"]
        ]).lower()

        if search_term in searchable_text:
            results.append(note)

    if len(results) == 0:
        print(f"\nNo notes found matching '{search_term}'.")
        return

    print(f"\nFound {len(results)} matching note(s).")

    for index, note in enumerate(results, start=1):
        display_note(note, index)


def main():
    notes = []

    print("=" * 50)
    print("INTEL NOTES MANAGER")
    print("=" * 50)
    print("Intelligence Note Management System")
    print("System initialized successfully.")

    while True:
        display_menu()

        choice = input("Select an option: ")

        if choice == "1":
            note = create_note()
            notes.append(note)

            print(f"Total notes in session: {len(notes)}")

        elif choice == "2":
            view_notes(notes)

        elif choice == "3":
            search_notes(notes)

        elif choice == "4":
            print("\nExiting Intel Notes Manager.")
            break

        else:
            print("\nInvalid selection. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()