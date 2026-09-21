import database


def get_total_notes():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM notes
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_discipline_distribution():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT discipline, COUNT(*)
        FROM notes
        GROUP BY discipline
        ORDER BY COUNT(*) DESC, discipline
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_classification_distribution():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT classification, COUNT(*)
        FROM notes
        GROUP BY classification
        ORDER BY COUNT(*) DESC, classification
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_reliability_distribution():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT reliability, COUNT(*)
        FROM notes
        GROUP BY reliability
        ORDER BY reliability
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_credibility_distribution():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT credibility, COUNT(*)
        FROM notes
        GROUP BY credibility
        ORDER BY credibility
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def display_distribution(title, results):
    print(f"\n{title}")
    print("-" * 60)

    if not results:
        print("No data available.")
        return

    for category, count in results:
        category_name = category if category else "NOT SPECIFIED"
        print(f"{category_name}: {count}")


def display_analytics():
    print("\n" + "=" * 60)
    print("INTELLIGENCE ANALYTICS")
    print("=" * 60)

    total = get_total_notes()

    print(f"\nTotal Intelligence Notes: {total}")

    if total == 0:
        print("\nNo intelligence data available for analysis.")
        print("=" * 60)
        return

    display_distribution(
        "INT DISCIPLINE DISTRIBUTION",
        get_discipline_distribution()
    )

    display_distribution(
        "CLASSIFICATION DISTRIBUTION",
        get_classification_distribution()
    )

    display_distribution(
        "SOURCE RELIABILITY DISTRIBUTION",
        get_reliability_distribution()
    )

    display_distribution(
        "INFORMATION CREDIBILITY DISTRIBUTION",
        get_credibility_distribution()
    )

    print("\n" + "=" * 60)