from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Classification = Literal[
    "UNCLASSIFIED",
    "CUI",
    "CONFIDENTIAL",
    "SECRET",
    "TOP SECRET",
]

Discipline = Literal[
    "HUMINT",
    "OSINT",
    "SIGINT",
    "GEOINT",
    "MASINT",
    "CYBINT",
    "ALL-SOURCE",
    "OTHER",
]

Reliability = Literal[
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
]

Credibility = Literal[
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
]


class IntelligenceNoteBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=250,
    )

    date: str | None = Field(
        default=None,
        max_length=10,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
    )

    source: str | None = Field(
        default=None,
        max_length=250,
    )

    classification: Classification | None = None
    discipline: Discipline | None = None

    location: str | None = Field(
        default=None,
        max_length=250,
    )

    tags: str | None = Field(
        default=None,
        max_length=500,
    )

    reliability: Reliability | None = None
    credibility: Credibility | None = None

    body: str | None = Field(
        default=None,
        max_length=20_000,
    )


class IntelligenceNoteCreate(IntelligenceNoteBase):
    pass


class IntelligenceNoteUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=250,
    )

    date: str | None = Field(
        default=None,
        max_length=10,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
    )

    source: str | None = Field(
        default=None,
        max_length=250,
    )

    classification: Classification | None = None
    discipline: Discipline | None = None

    location: str | None = Field(
        default=None,
        max_length=250,
    )

    tags: str | None = Field(
        default=None,
        max_length=500,
    )

    reliability: Reliability | None = None
    credibility: Credibility | None = None

    body: str | None = Field(
        default=None,
        max_length=20_000,
    )


class IntelligenceNoteResponse(IntelligenceNoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class DistributionItem(BaseModel):
    label: str
    count: int = Field(ge=0)


class AnalyticsResponse(BaseModel):
    total_notes: int = Field(ge=0)

    classification_distribution: list[DistributionItem] = Field(
        default_factory=list
    )

    discipline_distribution: list[DistributionItem] = Field(
        default_factory=list
    )

    reliability_distribution: list[DistributionItem] = Field(
        default_factory=list
    )

    credibility_distribution: list[DistributionItem] = Field(
        default_factory=list
    )

    source_evaluation_distribution: list[
        DistributionItem
    ] = Field(
        default_factory=list
    )

    location_distribution: list[DistributionItem] = Field(
        default_factory=list
    )

    tag_distribution: list[DistributionItem] = Field(
        default_factory=list
    )

    monthly_distribution: list[DistributionItem] = Field(
        default_factory=list
    )


class ExportMetadata(BaseModel):
    schema_name: Literal[
        "cin.intelligence-note"
    ] = "cin.intelligence-note"

    schema_version: Literal["1.0"] = "1.0"

    source_application: Literal[
        "Intel Notes Manager"
    ] = "Intel Notes Manager"

    application_version: Literal["2.0.0"] = "2.0.0"

    exported_at: datetime


class ExportedIntelligenceNote(BaseModel):
    record_identifier: str
    note_id: int

    title: str
    reporting_date: str | None = None
    source: str | None = None

    classification: Classification | None = None
    discipline: Discipline | None = None

    location: str | None = None
    tags: list[str] = Field(default_factory=list)

    reliability: Reliability | None = None
    credibility: Credibility | None = None
    source_evaluation: str | None = None

    narrative: str | None = None


class IntelligenceNoteExport(BaseModel):
    metadata: ExportMetadata
    record: ExportedIntelligenceNote


class IntelligenceNoteCollectionExport(BaseModel):
    metadata: ExportMetadata
    record_count: int = Field(ge=0)

    records: list[ExportedIntelligenceNote] = Field(
        default_factory=list
    )