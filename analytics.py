from collections import Counter

import database


# ============================================================
# TOTAL NOTES
# ============================================================

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


# ============================================================
# INT DISCIPLINE DISTRIBUTION
# ============================================================

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


# ============================================================
# CLASSIFICATION DISTRIBUTION
# ============================================================

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


# ============================================================
# SOURCE RELIABILITY DISTRIBUTION
# ============================================================

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


# ============================================================
# INFORMATION CREDIBILITY DISTRIBUTION
# ============================================================

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


# ============================================================
# SOURCE EVALUATION DISTRIBUTION
# ============================================================

def get_source_evaluation_distribution():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT reliability, credibility, COUNT(*)
        FROM notes
        WHERE reliability IS NOT NULL
          AND TRIM(reliability) != ''
          AND credibility IS NOT NULL
          AND TRIM(credibility) != ''
        GROUP BY reliability, credibility
        ORDER BY COUNT(*) DESC, reliability, credibility
    """)

    rows = cursor.fetchall()
    connection.close()

    results = []

    for reliability, credibility, count in rows:
        evaluation = f"{reliability}{credibility}"
        results.append((evaluation, count))

    return results


# ============================================================
# LOCATION DISTRIBUTION
# ============================================================

def get_location_distribution():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT location, COUNT(*)
        FROM notes
        WHERE location IS NOT NULL
          AND TRIM(location) != ''
        GROUP BY location
        ORDER BY COUNT(*) DESC, location
    """)

    results = cursor.fetchall()
    connection.close()

    return results


# ============================================================
# TAG DISTRIBUTION
# ============================================================

def get_tag_distribution():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT tags
        FROM notes
        WHERE tags IS NOT NULL
          AND TRIM(tags) != ''
    """)

    rows = cursor.fetchall()
    connection.close()

    tag_counter = Counter()

    for row in rows:
        tag_string = row[0]
        tags = tag_string.split(",")

        for tag in tags:
            normalized_tag = tag.strip().lower()

            if normalized_tag:
                tag_counter[normalized_tag] += 1

    return sorted(
        tag_counter.items(),
        key=lambda item: (-item[1], item[0])
    )


# ============================================================
# MONTHLY REPORTING DISTRIBUTION
# ============================================================

def get_monthly_distribution():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            SUBSTR(date, 1, 7) AS report_month,
            COUNT(*)
        FROM notes
        WHERE date IS NOT NULL
          AND TRIM(date) != ''
        GROUP BY report_month
        ORDER BY report_month
    """)

    results = cursor.fetchall()
    connection.close()

    return results


# ============================================================
# DISPLAY STANDARD DISTRIBUTION
# ============================================================

def display_distribution(title, results):
    print(f"\n{title}")
    print("-" * 60)

    if not results:
        print("No data available.")
        return

    for category, count in results:
        category_name = category if category else "NOT SPECIFIED"
        print(f"{category_name}: {count}")


# ============================================================
# DISPLAY MONTHLY REPORTING
# ============================================================

def display_monthly_distribution(results):
    print("\nREPORTING OVER TIME")
    print("-" * 60)

    if not results:
        print("No reporting dates available.")
        return

    for month, count in results:
        print(f"{month}: {count}")


# ============================================================
# DISPLAY ANALYTICS DASHBOARD
# ============================================================

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

    display_distribution(
        "SOURCE EVALUATION PAIRS",
        get_source_evaluation_distribution()
    )

    display_distribution(
        "TOP LOCATIONS",
        get_location_distribution()
    )

    display_distribution(
        "TOP TAGS",
        get_tag_distribution()
    )

    display_monthly_distribution(
        get_monthly_distribution()
    )

    print("\n" + "=" * 60)