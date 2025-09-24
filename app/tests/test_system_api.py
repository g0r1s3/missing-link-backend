# app/tests/test_system_api.py
from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _is_iso8601(value: str) -> bool:
    """
    Prüft robust auf ISO-8601 (mit Offset oder 'Z').
    """
    try:
        # Python <3.11 mag kein 'Z' → in +00:00 umschreiben
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        datetime.fromisoformat(value)
        return True
    except Exception:
        return False


def test_get_time() -> None:
    r = client.get("/api/v1/time")
    assert r.status_code == 200
    data = r.json()
    assert "server_time" in data
    assert isinstance(data["server_time"], str)
    assert _is_iso8601(data["server_time"])


def test_get_health() -> None:
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert "time" in data and _is_iso8601(data["time"])
    assert "services" in data and isinstance(data["services"], dict)
    assert data["services"].get("api") == "ok"


def test_get_version() -> None:
    r = client.get("/api/v1/version")
    assert r.status_code == 200
    data = r.json()
    # Minimalanforderungen
    assert "app" in data and isinstance(data["app"], str)
    assert "version" in data and isinstance(data["version"], str) and len(data["version"]) > 0
    # optionale Felder dürfen None sein
    assert "commit" in data
    assert "build_time" in data
    if data["build_time"] is not None:
        assert _is_iso8601(data["build_time"])
