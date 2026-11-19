from unittest.mock import AsyncMock, patch

from starlette.testclient import TestClient

from legko.db.base import Base
from legko.db.session import SessionLocal, engine
from legko.main import app
from legko.models import Campaign, SyncStatus


def test_home_shows_create_and_open():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "Создать кампанию" in response.text
    assert 'action="/campaigns/open"' in response.text
    assert "hx-get=\"/campaigns/search\"" in response.text


def test_open_by_id_redirects_to_editor():
    import random

    Base.metadata.create_all(bind=engine)
    kid = random.randint(900_000_001, 999_999_999)
    campaign = Campaign(
        keitaro_campaign_id=kid,
        name="Test",
        sync_status=SyncStatus.SYNCED,
    )
    db = SessionLocal()
    try:
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        local_id = campaign.id
    finally:
        db.close()

    with (
        TestClient(app) as client,
        patch("legko.web.routes_pages.KeitaroClient") as mock_cls,
    ):
        mock_cls.return_value.get_campaign = AsyncMock(return_value={"name": "Remote"})
        response = client.post(
            "/campaigns/open",
            data={"keitaro_campaign_id": str(kid)},
            follow_redirects=False,
        )
    assert response.status_code == 303
    assert response.headers["location"] == f"/campaigns/{local_id}/editor"