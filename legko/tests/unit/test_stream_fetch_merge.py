from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from legko.db.base import Base
from legko.models import Campaign, OfferStatus, Stream, StreamOffer, StreamType, SyncStatus
from legko.services.stream_fetch import full_fetch
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


def _seed_draft_campaign(session):
    campaign = Campaign(keitaro_campaign_id=42, name="Merge", sync_status=SyncStatus.DRAFT)
    session.add(campaign)
    session.flush()
    offer_stream = Stream(
        campaign_id=campaign.id,
        keitaro_stream_id=100,
        stream_type=StreamType.OFFER,
        has_draft=True,
    )
    session.add(offer_stream)
    session.flush()
    session.add(
        StreamOffer(
            stream_id=offer_stream.id,
            keitaro_offer_id=1,
            offer_name="Keitaro only",
            weight_percent=100,
            status=OfferStatus.ACTIVE,
        ),
    )
    session.flush()
    save_stream_snapshot(session, offer_stream)
    session.add(
        StreamOffer(
            stream_id=offer_stream.id,
            keitaro_offer_id=2,
            offer_name="Local add",
            weight_percent=50,
            status=OfferStatus.ACTIVE,
        ),
    )
    session.commit()
    return campaign, offer_stream


@pytest.mark.parametrize(
    "remote_offer_ids",
    [
        [1],
        [],
    ],
)
def test_merge_fetch_marks_missing_removed_and_keeps_local_add(db_session, remote_offer_ids):
    campaign, offer_stream = _seed_draft_campaign(db_session)
    client = MagicMock()
    client.list_campaign_streams = AsyncMock(
        return_value=[
            {
                "id": 100,
                "schema": "landings",
                "offers": [{"offer_id": oid, "share": 100, "state": "active"} for oid in remote_offer_ids],
            },
        ],
    )
    client.get_offer = AsyncMock(return_value=None)

    import asyncio

    asyncio.run(full_fetch(db_session, client, campaign))

    db_session.refresh(offer_stream)
    rows = {r.keitaro_offer_id: r for r in offer_stream.offers}
    assert rows[2].status == OfferStatus.ACTIVE
    if remote_offer_ids:
        assert rows[1].status == OfferStatus.ACTIVE
    else:
        assert rows[1].status == OfferStatus.REMOVED
    refreshed = db_session.get(Stream, offer_stream.id)
    assert refreshed is not None
    assert refreshed.has_draft is True


def test_full_fetch_without_draft_replaces(db_session):
    campaign = Campaign(keitaro_campaign_id=7, name="Cold", sync_status=SyncStatus.SYNCED)
    db_session.add(campaign)
    db_session.commit()

    client = MagicMock()
    client.list_campaign_streams = AsyncMock(
        return_value=[
            {"id": 9, "schema": "landings", "offers": [{"offer_id": 99, "share": 100, "state": "active"}]},
        ],
    )
    client.get_offer = AsyncMock(return_value={"name": "Remote"})

    import asyncio

    asyncio.run(full_fetch(db_session, client, campaign))

    from sqlalchemy import select

    streams = list(db_session.scalars(select(Stream).where(Stream.campaign_id == campaign.id)))
    assert len(streams) == 1
    offers = list(db_session.scalars(select(StreamOffer)))
    assert len(offers) == 1
    assert offers[0].keitaro_offer_id == 99