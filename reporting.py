import os
from datetime import datetime

import analytics


REPORTS_DIRECTORY = "reports"


def create_reports_directory():
    """
    Create the reports directory if it does not already exist.
    """
    os.makedirs(REPORTS_DIRECTORY, exist_ok=True)


def format_distribution(title, results):
    """
    Convert an analytics distribution into report-friendly text.
    """
    lines = [
        "",
        title,
        "-" * 60
    ]

    if not results:
        lines.append("No data available.")
        return lines

    for category, count in results:
        category_name = category if category else "NOT SPECIFIED"
        lines.append(f"{category_name}: {count}")

    return lines


def format_monthly_distribution(results):
    """
    Convert monthly reporting analytics into report-friendly text.
    """
    lines = [
        "",
        "REPORTING OVER TIME",
        "-" * 60
    ]

    if not results:
        lines.append("No reporting dates available.")
        return lines

    for month, count in results:
        lines.append(f"{month}: {count}")

    return lines


def build_analytics_report():
    """
    Build the complete intelligence analytics report as text.
    """
    total = analytics.get_total_notes()

    lines = [
        "=" * 60,
        "INTELLIGENCE ANALYTICS REPORT",
        "=" * 60,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Intelligence Notes: {total}"
    ]

    if total == 0:
        lines.extend([
            "",
            "No intelligence data available for analysis.",
            "=" * 60
        ])

        return "\n".join(lines)

    lines.extend(
        format_distribution(
            "INT DISCIPLINE DISTRIBUTION",
            analytics.get_discipline_distribution()
        )
    )

    lines.extend(
        format_distribution(
            "CLASSIFICATION DISTRIBUTION",
            analytics.get_classification_distribution()
        )
    )

    lines.extend(
        format_distribution(
            "SOURCE RELIABILITY DISTRIBUTION",
            analytics.get_reliability_distribution()
        )
    )

    lines.extend(
        format_distribution(
            "INFORMATION CREDIBILITY DISTRIBUTION",
            analytics.get_credibility_distribution()
        )
    )

    lines.extend(
        format_distribution(
            "SOURCE EVALUATION PAIRS",
            analytics.get_source_evaluation_distribution()
        )
    )

    lines.extend(
        format_distribution(
            "TOP LOCATIONS",
            analytics.get_location_distribution()
        )
    )

    lines.extend(
        format_distribution(
            "TOP TAGS",
            analytics.get_tag_distribution()
        )
    )

    lines.extend(
        format_monthly_distribution(
            analytics.get_monthly_distribution()
        )
    )

    lines.extend([
        "",
        "=" * 60
    ])

    return "\n".join(lines)


def generate_report_filename():
    """
    Generate a unique timestamped filename for an analytics report.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    return f"intelligence_analytics_{timestamp}.txt"


def export_analytics_report():
    """
    Export the current intelligence analytics to a text file.
    """
    create_reports_directory()

    report = build_analytics_report()
    filename = generate_report_filename()

    filepath = os.path.join(
        REPORTS_DIRECTORY,
        filename
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as report_file:
        report_file.write(report)

    return filepath