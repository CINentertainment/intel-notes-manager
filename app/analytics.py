from collections import Counter

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models, schemas


def build_distribution(
    database: Session,
    column,
) -> list[schemas.DistributionItem]:
    count_expression = func.count(
        models.IntelligenceNote.id
    )

    statement = (
        select(
            column,
            count_expression,
        )
        .where(column.is_not(None))
        .where(func.trim(column) != "")
        .group_by(column)
        .order_by(
            count_expression.desc(),
            column.asc(),
        )
    )

    rows = database.execute(statement).all()

    return [
        schemas.DistributionItem(
            label=str(label),
            count=count,
        )
        for label, count in rows
    ]


def build_location_distribution(
    database: Session,
) -> list[schemas.DistributionItem]:
    count_expression = func.count(
        models.IntelligenceNote.id
    )

    statement = (
        select(
            models.IntelligenceNote.location,
            count_expression,
        )
        .where(
            models.IntelligenceNote.location.is_not(None)
        )
        .where(
            func.trim(
                models.IntelligenceNote.location
            )
            != ""
        )
        .group_by(models.IntelligenceNote.location)
        .order_by(
            count_expression.desc(),
            models.IntelligenceNote.location.asc(),
        )
        .limit(10)
    )

    rows = database.execute(statement).all()

    return [
        schemas.DistributionItem(
            label=str(location),
            count=count,
        )
        for location, count in rows
    ]


def build_tag_distribution(
    database: Session,
) -> list[schemas.DistributionItem]:
    statement = (
        select(models.IntelligenceNote.tags)
        .where(models.IntelligenceNote.tags.is_not(None))
        .where(
            func.trim(models.IntelligenceNote.tags) != ""
        )
    )

    tag_values = database.scalars(statement).all()
    tag_counts: Counter[str] = Counter()

    for tag_value in tag_values:
        for tag in str(tag_value).split(","):
            normalized_tag = tag.strip().lower()

            if normalized_tag:
                tag_counts[normalized_tag] += 1

    sorted_tags = sorted(
        tag_counts.items(),
        key=lambda item: (
            -item[1],
            item[0],
        ),
    )[:10]

    return [
        schemas.DistributionItem(
            label=tag,
            count=count,
        )
        for tag, count in sorted_tags
    ]


def build_monthly_distribution(
    database: Session,
) -> list[schemas.DistributionItem]:
    statement = (
        select(models.IntelligenceNote.date)
        .where(models.IntelligenceNote.date.is_not(None))
        .where(
            func.trim(models.IntelligenceNote.date) != ""
        )
    )

    date_values = database.scalars(statement).all()
    month_counts: Counter[str] = Counter()

    for date_value in date_values:
        normalized_date = str(date_value).strip()

        if (
            len(normalized_date) >= 7
            and normalized_date[4] == "-"
        ):
            month_counts[normalized_date[:7]] += 1

    return [
        schemas.DistributionItem(
            label=month,
            count=month_counts[month],
        )
        for month in sorted(month_counts)
    ]


def build_source_evaluation_distribution(
    database: Session,
) -> list[schemas.DistributionItem]:
    statement = select(
        models.IntelligenceNote.reliability,
        models.IntelligenceNote.credibility,
    )

    rows = database.execute(statement).all()
    evaluation_counts: Counter[str] = Counter()

    for reliability, credibility in rows:
        if reliability and credibility:
            evaluation_code = (
                f"{reliability}{credibility}"
            )

            evaluation_counts[evaluation_code] += 1

    sorted_evaluations = sorted(
        evaluation_counts.items(),
        key=lambda item: (
            -item[1],
            item[0],
        ),
    )

    return [
        schemas.DistributionItem(
            label=evaluation,
            count=count,
        )
        for evaluation, count in sorted_evaluations
    ]


def build_analytics(
    database: Session,
) -> schemas.AnalyticsResponse:
    total_notes = database.scalar(
        select(
            func.count(models.IntelligenceNote.id)
        )
    )

    return schemas.AnalyticsResponse(
        total_notes=total_notes or 0,
        classification_distribution=build_distribution(
            database,
            models.IntelligenceNote.classification,
        ),
        discipline_distribution=build_distribution(
            database,
            models.IntelligenceNote.discipline,
        ),
        reliability_distribution=build_distribution(
            database,
            models.IntelligenceNote.reliability,
        ),
        credibility_distribution=build_distribution(
            database,
            models.IntelligenceNote.credibility,
        ),
        source_evaluation_distribution=(
            build_source_evaluation_distribution(
                database
            )
        ),
        location_distribution=(
            build_location_distribution(database)
        ),
        tag_distribution=build_tag_distribution(
            database
        ),
        monthly_distribution=(
            build_monthly_distribution(database)
        ),
    )