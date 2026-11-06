"""Tests for GET /health.

Unit tests replace the real database check with a fake, so they run anywhere.
The integration test talks to the real Postgres container and is marked separately.
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from groundtruth import main
from groundtruth.config import Settings, get_settings
from groundtruth.db import check_database

FAKE_SETTINGS = Settings(
    app_env="test",
    database_url="postgresql://user:pass@localhost:5999/never_used",
)


@pytest.fixture
def client() -> Iterator[TestClient]:
    """A test client whose settings never come from the developer's .env file."""
    main.app.dependency_overrides[get_settings] = lambda: FAKE_SETTINGS
    yield TestClient(main.app)
    main.app.dependency_overrides.clear()


def test_health_ok_when_database_up(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "check_database", lambda url: True)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "up", "environment": "test"}


def test_health_degraded_when_database_down(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(main, "check_database", lambda url: False)

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "database": "down", "environment": "test"}


def test_check_database_returns_false_for_unreachable_server() -> None:
    # Port 5999 has nothing listening, so the connection is refused quickly.
    assert check_database("postgresql://user:pass@127.0.0.1:5999/none", timeout_seconds=1) is False


@pytest.mark.integration
def test_real_database_is_reachable_and_has_pgvector() -> None:
    import psycopg

    url = str(get_settings().database_url)
    assert check_database(url) is True
    with psycopg.connect(url) as conn:
        row = conn.execute(
            "SELECT default_version FROM pg_available_extensions WHERE name = 'vector'"
        ).fetchone()
    assert row is not None, "pgvector extension is not available in this Postgres image"
