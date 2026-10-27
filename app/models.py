from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class IntelligenceNote(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    date: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    source: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    classification: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    discipline: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    tags: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    reliability: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    credibility: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    body: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )