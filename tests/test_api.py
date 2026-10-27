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

def test_dashboard():
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "Intel Notes Manager" in response.text
    assert 'id="noteForm"' in response.text
    assert 'id="noteList"' in response.text
    assert "/static/styles.css" in response.text
    assert "/static/app.js" in response.text


def test_dashboard_stylesheet():
    response = client.get("/static/styles.css")

    assert response.status_code == 200
    assert "--purple:" in response.text
    assert ".note-card" in response.text


def test_dashboard_javascript():
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert "initializeApplication" in response.text
    assert 'requestJson("/notes")' in response.text
def test_empty_analytics():
    response = client.get("/analytics")

    assert response.status_code == 200

    analytics = response.json()

    assert analytics["total_notes"] == 0
    assert analytics["classification_distribution"] == []
    assert analytics["discipline_distribution"] == []
    assert analytics["reliability_distribution"] == []
    assert analytics["credibility_distribution"] == []
    assert analytics["source_evaluation_distribution"] == []
    assert analytics["location_distribution"] == []
    assert analytics["tag_distribution"] == []
    assert analytics["monthly_distribution"] == []


def test_analytics_with_notes():
    first_note = sample_note(
        "First analytics note"
    )

    second_note = sample_note(
        "Second analytics note"
    )
    second_note.update(
        {
            "date": "2026-09-15",
            "classification": "SECRET",
            "discipline": "HUMINT",
            "location": "Austin, Texas",
            "tags": "facility, source",
            "reliability": "A",
            "credibility": "1",
        }
    )

    third_note = sample_note(
        "Third analytics note"
    )
    third_note.update(
        {
            "classification": "CUI",
            "tags": "facility, cyber",
        }
    )

    for note_data in [
        first_note,
        second_note,
        third_note,
    ]:
        response = client.post(
            "/notes",
            json=note_data,
        )

        assert response.status_code == 201

    response = client.get("/analytics")

    assert response.status_code == 200

    analytics = response.json()

    assert analytics["total_notes"] == 3

    classification_counts = {
        item["label"]: item["count"]
        for item in analytics[
            "classification_distribution"
        ]
    }

    assert classification_counts == {
        "UNCLASSIFIED": 1,
        "SECRET": 1,
        "CUI": 1,
    }

    discipline_counts = {
        item["label"]: item["count"]
        for item in analytics[
            "discipline_distribution"
        ]
    }

    assert discipline_counts == {
        "OSINT": 2,
        "HUMINT": 1,
    }

    evaluation_counts = {
        item["label"]: item["count"]
        for item in analytics[
            "source_evaluation_distribution"
        ]
    }

    assert evaluation_counts == {
        "B2": 2,
        "A1": 1,
    }

    location_counts = {
        item["label"]: item["count"]
        for item in analytics[
            "location_distribution"
        ]
    }

    assert location_counts == {
        "San Antonio, Texas": 2,
        "Austin, Texas": 1,
    }

    tag_counts = {
        item["label"]: item["count"]
        for item in analytics[
            "tag_distribution"
        ]
    }

    assert tag_counts["facility"] == 3
    assert tag_counts["cyber"] == 1
    assert tag_counts["source"] == 1
    assert tag_counts["surveillance"] == 1

    monthly_counts = {
        item["label"]: item["count"]
        for item in analytics[
            "monthly_distribution"
        ]
    }

    assert monthly_counts == {
        "2026-09": 1,
        "2026-10": 2,
    }
def test_note_report():
    note_data = sample_note(
        "Protective surveillance report"
    )
    note_data["body"] = (
        "Synthetic reporting indicates repeated activity "
        "near the identified facility."
    )

    create_response = client.post(
        "/notes",
        json=note_data,
    )

    assert create_response.status_code == 201

    note_id = create_response.json()["id"]

    response = client.get(
        f"/notes/{note_id}/report"
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "text/html"
    )
    assert "Protective surveillance report" in response.text
    assert "INTELLIGENCE NOTE REPORT" in response.text
    assert "Synthetic reporting indicates" in response.text
    assert "Print / Save as PDF" in response.text
    assert "INM-000001" in response.text


def test_note_report_for_missing_note():
    response = client.get("/notes/999/report")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Intelligence note not found.",
    }
def test_export_note():
    note_data = sample_note(
        "Exportable intelligence note"
    )
    note_data["tags"] = (
        "Facility, Surveillance, facility, Security"
    )

    create_response = client.post(
        "/notes",
        json=note_data,
    )

    assert create_response.status_code == 201

    note_id = create_response.json()["id"]

    response = client.get(
        f"/notes/{note_id}/export"
    )

    assert response.status_code == 200

    export_data = response.json()

    assert export_data["metadata"]["schema_name"] == (
        "cin.intelligence-note"
    )

    assert export_data["metadata"]["schema_version"] == "1.0"

    assert export_data["metadata"]["source_application"] == (
        "Intel Notes Manager"
    )

    assert export_data["metadata"]["application_version"] == (
        "2.0.0"
    )

    assert export_data["metadata"]["exported_at"]

    record = export_data["record"]

    assert record["record_identifier"] == "INM-000001"
    assert record["note_id"] == note_id
    assert record["title"] == (
        "Exportable intelligence note"
    )
    assert record["source_evaluation"] == "B2"

    assert record["tags"] == [
        "facility",
        "surveillance",
        "security",
    ]


def test_export_missing_note():
    response = client.get("/notes/999/export")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Intelligence note not found.",
    }


def test_export_all_notes():
    first_note = sample_note(
        "First exported note"
    )
    first_note["date"] = "2026-09-15"

    second_note = sample_note(
        "Second exported note"
    )
    second_note["date"] = "2026-10-22"

    for note_data in [
        first_note,
        second_note,
    ]:
        response = client.post(
            "/notes",
            json=note_data,
        )

        assert response.status_code == 201

    response = client.get("/exports/notes")

    assert response.status_code == 200

    export_data = response.json()

    assert export_data["metadata"]["schema_name"] == (
        "cin.intelligence-note"
    )

    assert export_data["record_count"] == 2
    assert len(export_data["records"]) == 2

    assert export_data["records"][0]["title"] == (
        "Second exported note"
    )

    assert export_data["records"][1]["title"] == (
        "First exported note"
    )
def test_import_exported_note():
    create_response = client.post(
        "/notes",
        json={
            "title": "Imported Intelligence Note",
            "date": "2026-10-27",
            "source": "External reporting",
            "classification": "UNCLASSIFIED",
            "discipline": "OSINT",
            "location": "San Antonio, Texas",
            "tags": "testing, interoperability",
            "reliability": "B",
            "credibility": "2",
            "body": (
                "This note verifies the standardized "
                "JSON import workflow."
            ),
        },
    )

    assert create_response.status_code == 201

    note_id = create_response.json()["id"]

    export_response = client.get(
        f"/notes/{note_id}/export"
    )

    assert export_response.status_code == 200

    delete_response = client.delete(
        f"/notes/{note_id}"
    )

    assert delete_response.status_code == 204

    import_response = client.post(
        "/imports/notes",
        json=export_response.json(),
    )

    assert import_response.status_code == 201

    imported_note = import_response.json()

    assert imported_note["title"] == (
        "Imported Intelligence Note"
    )
    assert imported_note["date"] == "2026-10-27"
    assert imported_note["discipline"] == "OSINT"
    assert imported_note["reliability"] == "B"
    assert imported_note["credibility"] == "2"
    assert imported_note["tags"] == (
        "testing, interoperability"
    )


def test_reject_duplicate_import():
    create_response = client.post(
        "/notes",
        json={
            "title": "Duplicate Import Test",
            "date": "2026-10-27",
            "classification": "UNCLASSIFIED",
            "discipline": "OSINT",
            "tags": "duplicate, testing",
            "reliability": "A",
            "credibility": "1",
            "body": "Duplicate import test narrative.",
        },
    )

    assert create_response.status_code == 201

    note_id = create_response.json()["id"]

    export_response = client.get(
        f"/notes/{note_id}/export"
    )

    assert export_response.status_code == 200

    import_response = client.post(
        "/imports/notes",
        json=export_response.json(),
    )

    assert import_response.status_code == 409
    assert import_response.json() == {
        "detail": (
            "This intelligence note has already "
            "been imported."
        )
    }


def test_reject_invalid_import():
    response = client.post(
        "/imports/notes",
        json={},
    )

    assert response.status_code == 422