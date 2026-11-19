from sqlalchemy import delete
from sqlalchemy.orm import Session

from legko.integrations.keitaro.client import KeitaroClient, KeitaroError
from legko.models import Campaign, OfferStatus, Stream, StreamOffer, StreamType, SyncStatus


def _classify_stream(remote: dict) -> StreamType:
    if remote.get("offers"):
        return StreamType.OFFER
    if remote.get("schema") == "landings":
        return StreamType.OFFER
    return StreamType.SERVICE


async def full_fetch(db: Session, client: KeitaroClient, campaign: Campaign) -> None:
    if campaign.keitaro_campaign_id is None:
        raise KeitaroError("У кампании нет Keitaro ID")

    remote_streams = await client.list_campaign_streams(campaign.keitaro_campaign_id)

    db.execute(delete(Stream).where(Stream.campaign_id == campaign.id))

    for remote in remote_streams:
        keitaro_stream_id = remote.get("id")
        if keitaro_stream_id is None:
            continue
        stream = Stream(
            campaign_id=campaign.id,
            keitaro_stream_id=int(keitaro_stream_id),
            stream_type=_classify_stream(remote),
            has_draft=False,
        )
        db.add(stream)
        db.flush()

        if stream.stream_type != StreamType.OFFER:
            continue

        for row in remote.get("offers") or []:
            if not isinstance(row, dict):
                continue
            oid = row.get("offer_id")
            if oid is None:
                continue
            share = row.get("share")
            weight = int(share) if share is not None else 0
            offer_name: str | None = None
            try:
                remote_offer = await client.get_offer(int(oid))
                if remote_offer:
                    offer_name = (remote_offer.get("name") or "")[:512] or None
            except KeitaroError:
                offer_name = None
            db.add(
                StreamOffer(
                    stream_id=stream.id,
                    keitaro_offer_id=int(oid),
                    offer_name=offer_name,
                    weight_percent=weight,
                    is_pinned=False,
                    pinned_percent=None,
                    status=OfferStatus.ACTIVE,
                ),
            )

    campaign.sync_status = SyncStatus.SYNCED
    db.commit()
    db.refresh(campaign)