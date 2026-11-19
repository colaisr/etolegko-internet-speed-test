from starlette.testclient import TestClient

from legko.db.base import Base
from legko.db.session import engine
from legko.main import app


def test_health_degraded_without_keitaro_key(monkeypatch):
    monkeypatch.setenv("KEITARO_API_KEY", "")
    from legko.settings import get_settings

    get_settings.cache_clear()

    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 503
    payload = response.json()
    assert payload["database"]["ok"] is True
    assert payload["keitaro"]["ok"] is False
    assert "KEITARO_API_KEY" in payload["keitaro"]["message"]

    get_settings.cache_clear()