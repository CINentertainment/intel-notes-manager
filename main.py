import database
from analytics import display_analytics
from notes import (
    create_note,
    delete_note,
    edit_note,
    view_notes,
)
from reporting import export_analytics_report
from search import search_notes


def display_menu():
    print("\n" + "=" * 60)
    print("INTEL NOTES MANAGER")
    print("=" * 60)
    print("1. Create Intelligence Note")
    print("2. View Intelligence Notes")
    print("3. Search & Filter Intelligence Notes")
    print("4. Edit Intelligence Note")
    print("5. Delete Intelligence Note")
    print("6. Intelligence Analytics")
    print("7. Export Analytics Report")
    print("8. Exit")
    print("=" * 60)


def export_report():
    print("\n" + "=" * 60)
    print("EXPORT ANALYTICS REPORT")
    print("=" * 60)

    try:
        filepath = export_analytics_report()

        print("\nAnalytics report exported successfully.")
        print(f"Saved to: {filepath}")

    except Exception as error:
        print("\nUnable to export analytics report.")
        print(f"Error: {error}")


def main():
    database.create_database()

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
            display_analytics()

        elif choice == "7":
            export_report()

        elif choice == "8":
            print("\nExiting Intel Notes Manager.")
            break

        else:
            print(
                "\nInvalid selection. "
                "Please enter 1 through 8."
            )


if __name__ == "__main__":
    main()