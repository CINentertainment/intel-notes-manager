from collections.abc import Sequence
from datetime import datetime, timezone

from app import models, schemas


def normalize_tags(
    tags: str | None,
) -> list[str]:
    if not tags:
        return []

    normalized_tags = []
    seen_tags = set()

    for tag in tags.split(","):
        normalized_tag = tag.strip().lower()

        if (
            normalized_tag
            and normalized_tag not in seen_tags
        ):
            normalized_tags.append(normalized_tag)
            seen_tags.add(normalized_tag)

    return normalized_tags


def build_source_evaluation(
    reliability: str | None,
    credibility: str | None,
) -> str | None:
    if not reliability and not credibility:
        return None

    reliability_code = reliability or "—"
    credibility_code = credibility or "—"

    return f"{reliability_code}{credibility_code}"


def build_export_metadata(
    exported_at: datetime | None = None,
) -> schemas.ExportMetadata:
    return schemas.ExportMetadata(
        exported_at=(
            exported_at
            or datetime.now(timezone.utc)
        )
    )


def build_export_record(
    note: models.IntelligenceNote,
) -> schemas.ExportedIntelligenceNote:
    return schemas.ExportedIntelligenceNote(
        record_identifier=f"INM-{note.id:06d}",
        note_id=note.id,
        title=note.title,
        reporting_date=note.date,
        source=note.source,
        classification=note.classification,
        discipline=note.discipline,
        location=note.location,
        tags=normalize_tags(note.tags),
        reliability=note.reliability,
        credibility=note.credibility,
        source_evaluation=build_source_evaluation(
            note.reliability,
            note.credibility,
        ),
        narrative=note.body,
    )


def build_note_export(
    note: models.IntelligenceNote,
) -> schemas.IntelligenceNoteExport:
    exported_at = datetime.now(timezone.utc)

    return schemas.IntelligenceNoteExport(
        metadata=build_export_metadata(
            exported_at
        ),
        record=build_export_record(note),
    )


def build_collection_export(
    notes: Sequence[models.IntelligenceNote],
) -> schemas.IntelligenceNoteCollectionExport:
    exported_at = datetime.now(timezone.utc)

    records = [
        build_export_record(note)
        for note in notes
    ]

    return schemas.IntelligenceNoteCollectionExport(
        metadata=build_export_metadata(
            exported_at
        ),
        record_count=len(records),
        records=records,
    )
def build_import_data(
    record: schemas.ExportedIntelligenceNote,
) -> dict:
    tags = ", ".join(record.tags) or None

    return {
        "title": record.title,
        "date": record.reporting_date,
        "source": record.source,
        "classification": record.classification,
        "discipline": record.discipline,
        "location": record.location,
        "tags": tags,
        "reliability": record.reliability,
        "credibility": record.credibility,
        "body": record.narrative,
    }