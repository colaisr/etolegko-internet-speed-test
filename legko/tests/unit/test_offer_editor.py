import random
from unittest.mock import AsyncMock, patch

from starlette.testclient import TestClient

from legko.db.base import Base
from legko.db.session import SessionLocal, engine
from legko.main import app
from legko.models import Campaign, OfferStatus, Stream, StreamOffer, StreamType, SyncStatus
from legko.services.offer_editor import add_offer, remove_offer, restore_offer, set_pin


def _seed_campaign_with_offers():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    kid = random.randint(910_000_001, 919_999_999)
    campaign = Campaign(keitaro_campaign_id=kid, name="Ops", geo_code="DE", sync_status=SyncStatus.SYNCED)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    offer_stream = Stream(
        campaign_id=campaign.id,
        stream_type=StreamType.OFFER,
        keitaro_stream_id=1,
        has_draft=False,
    )
    db.add(offer_stream)
    db.flush()
    row = StreamOffer(
        stream_id=offer_stream.id,
        keitaro_offer_id=100,
        offer_name="One",
        weight_percent=100,
        status=OfferStatus.ACTIVE,
    )
    db.add(row)
    db.commit()
    return campaign.id, offer_stream.id, row.id


def test_remove_and_restore_recalculates():
    campaign_id, stream_id, row_id = _seed_campaign_with_offers()
    db = SessionLocal()
    try:
        row2 = StreamOffer(
            stream_id=stream_id,
            keitaro_offer_id=101,
            offer_name="Two",
            weight_percent=0,
            status=OfferStatus.ACTIVE,
        )
        db.add(row2)
        db.commit()
        from legko.services.offer_editor import recalculate_stream_offers

        stream = db.get(Stream, stream_id)
        recalculate_stream_offers(list(stream.offers))
        db.commit()

        remove_offer(db, campaign_id, row_id)
        campaign = db.get(Campaign, campaign_id)
        stream = db.query(Stream).filter_by(campaign_id=campaign_id, stream_type=StreamType.OFFER).one()
        assert stream.has_draft is True
        assert campaign.sync_status == SyncStatus.DRAFT
        active = [o for o in stream.offers if o.status == OfferStatus.ACTIVE]
        assert len(active) == 1
        assert active[0].weight_percent == 100

        restore_offer(db, campaign_id, row_id)
        stream = db.query(Stream).filter_by(campaign_id=campaign_id, stream_type=StreamType.OFFER).one()
        active = [o for o in stream.offers if o.status == OfferStatus.ACTIVE]
        assert sum(o.weight_percent for o in active) == 100
    finally:
        db.close()


def test_pin_25_splits_rest():
    campaign_id, stream_id, row1 = _seed_campaign_with_offers()
    db = SessionLocal()
    try:
        row2 = StreamOffer(
            stream_id=stream_id,
            keitaro_offer_id=102,
            offer_name="B",
            weight_percent=0,
            status=OfferStatus.ACTIVE,
        )
        db.add(row2)
        db.commit()
        from legko.services.offer_editor import recalculate_stream_offers

        stream = db.get(Stream, stream_id)
        recalculate_stream_offers(list(stream.offers))
        db.commit()

        pinned_row = db.get(StreamOffer, row1)
        set_pin(db, campaign_id, pinned_row.id, enabled=True, percent=25)
        db.expire_all()
        pinned_row = db.get(StreamOffer, row1)
        stream = db.query(Stream).filter_by(campaign_id=campaign_id, stream_type=StreamType.OFFER).one()
        active = [o for o in stream.offers if o.status == OfferStatus.ACTIVE]
        assert sum(o.weight_percent for o in active) == 100
        assert pinned_row.weight_percent == 25
    finally:
        db.close()


def test_editor_add_offer_route():
    campaign_id, _, _ = _seed_campaign_with_offers()
    with (
        TestClient(app) as client,
        patch("legko.web.routes_pages.KeitaroClient") as mock_cls,
    ):
        mock_cls.return_value.get_offer = AsyncMock(return_value={"name": "NewOffer"})
        response = client.post(
            f"/campaigns/{campaign_id}/offers",
            data={"offer_id": "200"},
            follow_redirects=False,
        )
    assert response.status_code == 303