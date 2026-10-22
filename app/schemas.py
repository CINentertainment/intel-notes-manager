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