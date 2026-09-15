from database import create_database

from notes import (
    create_note,
    delete_note,
    edit_note,
    view_notes
)

from search import search_notes


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