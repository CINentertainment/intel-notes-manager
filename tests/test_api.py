import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


def override_get_db():
    database = TestingSessionLocal()

    try:
        yield database
    finally:
        database.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


def sample_note(
    title: str = "Suspicious activity near facility",
) -> dict:
    return {
        "title": title,
        "date": "2026-10-22",
        "source": "Public safety bulletin",
        "classification": "UNCLASSIFIED",
        "discipline": "OSINT",
        "location": "San Antonio, Texas",
        "tags": "facility, surveillance, security",
        "reliability": "B",
        "credibility": "2",
        "body": (
            "A public safety bulletin reported suspicious "
            "activity near a protected facility."
        ),
    }


def create_test_note(
    title: str = "Suspicious activity near facility",
) -> dict:
    response = client.post(
        "/notes",
        json=sample_note(title),
    )

    assert response.status_code == 201

    return response.json()


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "application": "Intel Notes Manager",
        "status": "operational",
        "version": "2.0.0",
    }


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }


def test_create_note():
    response = client.post(
        "/notes",
        json=sample_note(),
    )

    assert response.status_code == 201

    created_note = response.json()

    assert created_note["id"] == 1
    assert (
        created_note["title"]
        == "Suspicious activity near facility"
    )
    assert created_note["classification"] == "UNCLASSIFIED"
    assert created_note["discipline"] == "OSINT"
    assert created_note["reliability"] == "B"
    assert created_note["credibility"] == "2"


def test_list_notes():
    first_note = create_test_note(
        "First intelligence note"
    )

    second_note = create_test_note(
        "Second intelligence note"
    )

    response = client.get("/notes")

    assert response.status_code == 200

    notes = response.json()

    assert len(notes) == 2
    assert notes[0]["id"] == second_note["id"]
    assert notes[1]["id"] == first_note["id"]


def test_get_note():
    created_note = create_test_note()

    response = client.get(
        f"/notes/{created_note['id']}"
    )

    assert response.status_code == 200
    assert response.json() == created_note


def test_get_missing_note():
    response = client.get("/notes/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Intelligence note not found.",
    }


def test_update_note():
    created_note = create_test_note()

    response = client.patch(
        f"/notes/{created_note['id']}",
        json={
            "title": "Updated intelligence note",
            "reliability": "A",
            "credibility": "1",
        },
    )

    assert response.status_code == 200

    updated_note = response.json()

    assert updated_note["title"] == (
        "Updated intelligence note"
    )
    assert updated_note["reliability"] == "A"
    assert updated_note["credibility"] == "1"
    assert updated_note["location"] == (
        "San Antonio, Texas"
    )


def test_update_missing_note():
    response = client.patch(
        "/notes/999",
        json={
            "title": "Missing note",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Intelligence note not found.",
    }


def test_delete_note():
    created_note = create_test_note()
    note_id = created_note["id"]

    delete_response = client.delete(
        f"/notes/{note_id}"
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(
        f"/notes/{note_id}"
    )

    assert get_response.status_code == 404


def test_filter_notes_by_keyword():
    create_test_note(
        "Suspicious surveillance activity"
    )

    create_test_note(
        "Cybersecurity incident report"
    )

    response = client.get(
        "/notes",
        params={"keyword": "cybersecurity"},
    )

    assert response.status_code == 200

    notes = response.json()

    assert len(notes) == 1
    assert notes[0]["title"] == (
        "Cybersecurity incident report"
    )


def test_filter_notes_by_classification():
    create_test_note()

    secret_note = sample_note(
        "Restricted intelligence report"
    )
    secret_note["classification"] = "SECRET"

    create_response = client.post(
        "/notes",
        json=secret_note,
    )

    assert create_response.status_code == 201

    response = client.get(
        "/notes",
        params={"classification": "SECRET"},
    )

    assert response.status_code == 200

    notes = response.json()

    assert len(notes) == 1
    assert notes[0]["classification"] == "SECRET"


def test_filter_notes_by_date_range():
    first_note = sample_note(
        "Earlier intelligence note"
    )
    first_note["date"] = "2026-09-15"

    second_note = sample_note(
        "Current intelligence note"
    )
    second_note["date"] = "2026-10-22"

    third_note = sample_note(
        "Later intelligence note"
    )
    third_note["date"] = "2026-11-10"

    assert client.post(
        "/notes",
        json=first_note,
    ).status_code == 201

    assert client.post(
        "/notes",
        json=second_note,
    ).status_code == 201

    assert client.post(
        "/notes",
        json=third_note,
    ).status_code == 201

    response = client.get(
        "/notes",
        params={
            "start_date": "2026-10-01",
            "end_date": "2026-10-31",
        },
    )

    assert response.status_code == 200

    notes = response.json()

    assert len(notes) == 1
    assert notes[0]["title"] == (
        "Current intelligence note"
    )


def test_reject_invalid_classification():
    note_data = sample_note()
    note_data["classification"] = "INVALID"

    response = client.post(
        "/notes",
        json=note_data,
    )

    assert response.status_code == 422


def test_reject_invalid_date_format():
    note_data = sample_note()
    note_data["date"] = "10/22/2026"

    response = client.post(
        "/notes",
        json=note_data,
    )

    assert response.status_code == 422


def test_reject_null_title_during_update():
    created_note = create_test_note()

    response = client.patch(
        f"/notes/{created_note['id']}",
        json={
            "title": None,
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "title cannot be null.",
    }