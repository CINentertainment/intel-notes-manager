from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Intel Notes Manager",
    description=(
        "A structured intelligence note-management API for recording, "
        "searching, evaluating, and organizing intelligence information."
    ),
    version="2.0.0",
)


def get_note_or_404(
    note_id: int,
    database: Session,
) -> models.IntelligenceNote:
    note = database.get(
        models.IntelligenceNote,
        note_id,
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intelligence note not found.",
        )

    return note


@app.get("/")
def read_root():
    return {
        "application": "Intel Notes Manager",
        "status": "operational",
        "version": "2.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.post(
    "/notes",
    response_model=schemas.IntelligenceNoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    note_data: schemas.IntelligenceNoteCreate,
    database: Session = Depends(get_db),
):
    note = models.IntelligenceNote(
        **note_data.model_dump()
    )

    database.add(note)
    database.commit()
    database.refresh(note)

    return note


@app.get(
    "/notes",
    response_model=list[schemas.IntelligenceNoteResponse],
)
def list_notes(
    keyword: str | None = None,
    classification: schemas.Classification | None = None,
    discipline: schemas.Discipline | None = None,
    reliability: schemas.Reliability | None = None,
    credibility: schemas.Credibility | None = None,
    location: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    database: Session = Depends(get_db),
):
    statement = select(models.IntelligenceNote)

    if keyword:
        search_term = f"%{keyword.strip()}%"

        statement = statement.where(
            or_(
                models.IntelligenceNote.title.ilike(
                    search_term
                ),
                models.IntelligenceNote.body.ilike(
                    search_term
                ),
                models.IntelligenceNote.source.ilike(
                    search_term
                ),
                models.IntelligenceNote.location.ilike(
                    search_term
                ),
                models.IntelligenceNote.tags.ilike(
                    search_term
                ),
            )
        )

    if classification:
        statement = statement.where(
            models.IntelligenceNote.classification
            == classification
        )

    if discipline:
        statement = statement.where(
            models.IntelligenceNote.discipline
            == discipline
        )

    if reliability:
        statement = statement.where(
            models.IntelligenceNote.reliability
            == reliability
        )

    if credibility:
        statement = statement.where(
            models.IntelligenceNote.credibility
            == credibility
        )

    if location:
        statement = statement.where(
            models.IntelligenceNote.location.ilike(
                f"%{location.strip()}%"
            )
        )

    if start_date:
        statement = statement.where(
            models.IntelligenceNote.date >= start_date
        )

    if end_date:
        statement = statement.where(
            models.IntelligenceNote.date <= end_date
        )

    statement = statement.order_by(
        models.IntelligenceNote.date.desc(),
        models.IntelligenceNote.id.desc(),
    )

    return database.scalars(statement).all()


@app.get(
    "/notes/{note_id}",
    response_model=schemas.IntelligenceNoteResponse,
)
def get_note(
    note_id: int,
    database: Session = Depends(get_db),
):
    return get_note_or_404(
        note_id,
        database,
    )


@app.patch(
    "/notes/{note_id}",
    response_model=schemas.IntelligenceNoteResponse,
)
def update_note(
    note_id: int,
    note_data: schemas.IntelligenceNoteUpdate,
    database: Session = Depends(get_db),
):
    note = get_note_or_404(
        note_id,
        database,
    )

    changes = note_data.model_dump(
        exclude_unset=True
    )

    if (
        "title" in changes
        and changes["title"] is None
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="title cannot be null.",
        )

    for field_name, value in changes.items():
        setattr(
            note,
            field_name,
            value,
        )

    database.commit()
    database.refresh(note)

    return note


@app.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    note_id: int,
    database: Session = Depends(get_db),
):
    note = get_note_or_404(
        note_id,
        database,
    )

    database.delete(note)
    database.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )