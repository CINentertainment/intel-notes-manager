from datetime import datetime

from database import get_connection
from notes import display_results

from validation import (
    get_classification,
    get_credibility,
    get_discipline,
    get_reliability,
    get_valid_date
)


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

    connection = get_connection()
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

    connection = get_connection()
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
# INT DISCIPLINE FILTER
# ============================================================

def filter_by_discipline():
    print("\n" + "=" * 60)
    print("FILTER BY INT DISCIPLINE")
    print("=" * 60)

    discipline = get_discipline()

    connection = get_connection()
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

    connection = get_connection()
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

    connection = get_connection()
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

    connection = get_connection()
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

    connection = get_connection()
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

    connection = get_connection()
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