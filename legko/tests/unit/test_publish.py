import asyncio
import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from legko.db.base import Base
from legko.models import Campaign, OfferStatus, Stream, StreamOffer, StreamType, SyncStatus
from legko.services.publish import PublishError, cancel_draft, push_to_keitaro
from legko.services.stream_snapshot import save_stream_snapshot


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def _seed_draft(session: Session) -> tuple[uuid.UUID, Stream]:
    campaign = Campaign(
        keitaro_campaign_id=99,
        name="Test",
        sync_status=SyncStatus.DRAFT,
    )
    session.add(campaign)
    session.flush()
    stream = Stream(
        campaign_id=campaign.id,
        keitaro_stream_id=555,
        stream_type=StreamType.OFFER,
        has_draft=True,
    )
    session.add(stream)
    session.flush()
    session.add(
        StreamOffer(
            stream_id=stream.id,
            keitaro_offer_id=10,
            weight_percent=100,
            status=OfferStatus.ACTIVE,
        ),
    )
    session.flush()
    save_stream_snapshot(session, stream)
    session.commit()
    return campaign.id, stream


def test_push_updates_keitaro_and_clears_draft(db_session):
    campaign_id, stream = _seed_draft(db_session)
    client = MagicMock()
    client.update_stream_offers = AsyncMock()

    async def run():
        await push_to_keitaro(db_session, client, campaign_id)

    asyncio.run(run())
    client.update_stream_offers.assert_awaited_once_with(555, [(10, 100)])
    refreshed = db_session.get(Stream, stream.id)
    assert refreshed is not None
    assert refreshed.has_draft is False


def test_cancel_restores_snapshot(db_session):
    campaign_id, stream = _seed_draft(db_session)
    from sqlalchemy import select

    row = db_session.scalars(select(StreamOffer).where(StreamOffer.stream_id == stream.id)).one()
    row.weight_percent = 70
    db_session.add(
        StreamOffer(
            stream_id=stream.id,
            keitaro_offer_id=11,
            weight_percent=30,
            status=OfferStatus.ACTIVE,
        ),
    )
    db_session.commit()
    cancel_draft(db_session, campaign_id)
    rows = list(db_session.scalars(select(StreamOffer).where(StreamOffer.stream_id == stream.id)))
    assert len(rows) == 1
    assert rows[0].keitaro_offer_id == 10
    assert rows[0].weight_percent == 100
    assert db_session.get(Stream, stream.id).has_draft is False


def test_cancel_without_snapshot_raises(db_session):
    campaign = Campaign(keitaro_campaign_id=1, name="x", sync_status=SyncStatus.DRAFT)
    db_session.add(campaign)
    db_session.flush()
    stream = Stream(
        campaign_id=campaign.id,
        stream_type=StreamType.OFFER,
        has_draft=True,
        keitaro_stream_id=1,
    )
    db_session.add(stream)
    db_session.commit()
    with pytest.raises(PublishError):
        cancel_draft(db_session, campaign.id)