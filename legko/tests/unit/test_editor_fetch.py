from unittest.mock import AsyncMock, patch

from starlette.testclient import TestClient

from legko.db.base import Base
from legko.db.session import SessionLocal, engine
from legko.main import app
from legko.models import Campaign, OfferStatus, Stream, StreamOffer, StreamType, SyncStatus
from legko.services.editor_view import editor_context


def test_editor_context_sums_active_weights():
    campaign = Campaign(keitaro_campaign_id=1, name="T", geo_code="DE")
    offer_stream = Stream(stream_type=StreamType.OFFER)
    offer_stream.offers = [
        StreamOffer(keitaro_offer_id=1, weight_percent=60, status=OfferStatus.ACTIVE),
        StreamOffer(keitaro_offer_id=2, weight_percent=0, status=OfferStatus.REMOVED),
        StreamOffer(keitaro_offer_id=3, weight_percent=40, status=OfferStatus.ACTIVE),
    ]
    campaign.streams = [
        Stream(stream_type=StreamType.SERVICE),
        offer_stream,
    ]
    ctx = editor_context(campaign)
    assert ctx["active_weight_sum"] == 100
    assert ctx["has_streams"] is True
    assert "DE" in ctx["service_stream_label"]


def test_editor_page_renders_offer_table():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        campaign = Campaign(
            keitaro_campaign_id=880_001,
            name="Editor test",
            geo_code="US",
            sync_status=SyncStatus.SYNCED,
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        svc = Stream(
            campaign_id=campaign.id,
            stream_type=StreamType.SERVICE,
            keitaro_stream_id=10,
        )
        offer_stream = Stream(
            campaign_id=campaign.id,
            stream_type=StreamType.OFFER,
            keitaro_stream_id=11,
        )
        db.add_all([svc, offer_stream])
        db.flush()
        db.add(
            StreamOffer(
                stream_id=offer_stream.id,
                keitaro_offer_id=18813,
                offer_name="Flexacil",
                weight_percent=100,
                status=OfferStatus.ACTIVE,
            ),
        )
        db.commit()
        local_id = campaign.id
    finally:
        db.close()

    with TestClient(app) as client:
        response = client.get(f"/campaigns/{local_id}/editor")
    assert response.status_code == 200
    assert "Ротация офферов" in response.text
    assert "Flexacil" in response.text
    assert "Fetch Streams" in response.text
    assert "Служебный поток" in response.text


def test_editor_empty_streams_shows_fetch_cta():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        campaign = Campaign(
            keitaro_campaign_id=880_002,
            name="Empty",
            sync_status=SyncStatus.NEEDS_FETCH,
        )
        db.add(campaign)
        db.commit()
        local_id = campaign.id
    finally:
        db.close()

    with TestClient(app) as client:
        response = client.get(f"/campaigns/{local_id}/editor")
    assert response.status_code == 200
    assert "Потоки ещё не загружены" in response.text


def test_fetch_post_redirects_to_editor():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        campaign = Campaign(keitaro_campaign_id=880_003, name="Fetch me")
        db.add(campaign)
        db.commit()
        local_id = campaign.id
    finally:
        db.close()

    with (
        TestClient(app) as client,
        patch("legko.web.routes_pages.full_fetch", new_callable=AsyncMock) as mock_fetch,
    ):
        response = client.post(
            f"/campaigns/{local_id}/fetch",
            follow_redirects=False,
        )
    assert response.status_code == 303
    assert response.headers["location"] == f"/campaigns/{local_id}/editor"
    mock_fetch.assert_awaited_once()