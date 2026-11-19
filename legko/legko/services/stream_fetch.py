from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from legko.integrations.keitaro.client import KeitaroClient, KeitaroError
from legko.models import Campaign, OfferStatus, Stream, StreamOffer, StreamType, SyncStatus
from legko.services.editor_view import load_campaign_for_editor
from legko.services.offer_editor import recalculate_stream_offers
from legko.services.stream_snapshot import load_snapshot_payload, save_stream_snapshot


def _classify_stream(remote: dict) -> StreamType:
    if remote.get("offers"):
        return StreamType.OFFER
    if remote.get("schema") == "landings":
        return StreamType.OFFER
    return StreamType.SERVICE


def _find_remote_offer_stream(remote_streams: list[dict]) -> dict | None:
    for remote in remote_streams:
        if _classify_stream(remote) == StreamType.OFFER:
            return remote
    return None


def _remote_active_offer_ids(remote_offer_stream: dict) -> set[int]:
    ids: set[int] = set()
    for row in remote_offer_stream.get("offers") or []:
        if not isinstance(row, dict):
            continue
        oid = row.get("offer_id")
        if oid is None:
            continue
        state = (row.get("state") or "active").lower()
        if state == "disabled":
            continue
        ids.add(int(oid))
    return ids


async def _refresh_offer_name(client: KeitaroClient, offer_id: int) -> str | None:
    try:
        remote_offer = await client.get_offer(offer_id)
    except KeitaroError:
        return None
    if remote_offer:
        return (remote_offer.get("name") or "")[:512] or None
    return None


async def _sync_service_streams(
    db: Session,
    campaign: Campaign,
    remote_streams: list[dict],
) -> None:
    db.execute(
        delete(Stream).where(
            Stream.campaign_id == campaign.id,
            Stream.stream_type == StreamType.SERVICE,
        ),
    )
    for remote in remote_streams:
        if _classify_stream(remote) == StreamType.OFFER:
            continue
        keitaro_stream_id = remote.get("id")
        if keitaro_stream_id is None:
            continue
        db.add(
            Stream(
                campaign_id=campaign.id,
                keitaro_stream_id=int(keitaro_stream_id),
                stream_type=StreamType.SERVICE,
                has_draft=False,
            ),
        )


async def _merge_fetch_preserve_draft(
    db: Session,
    client: KeitaroClient,
    campaign: Campaign,
    offer_stream: Stream,
    remote_streams: list[dict],
) -> None:
    """F7: при черновике не затирать локальный микс; пропавшие в Keitaro → removed."""
    remote_offer = _find_remote_offer_stream(remote_streams)
    if remote_offer is None:
        raise KeitaroError("В Keitaro нет оффер-потока")

    remote_id = remote_offer.get("id")
    if remote_id is not None:
        offer_stream.keitaro_stream_id = int(remote_id)

    remote_ids = _remote_active_offer_ids(remote_offer)
    snapshot = load_snapshot_payload(db, offer_stream.id) or []
    keitaro_baseline_active = {
        int(row["keitaro_offer_id"])
        for row in snapshot
        if row.get("status") == OfferStatus.ACTIVE.value
    }
    changed = False

    for local in list(offer_stream.offers or []):
        if local.keitaro_offer_id in remote_ids:
            if not local.offer_name:
                name = await _refresh_offer_name(client, local.keitaro_offer_id)
                if name:
                    local.offer_name = name
            continue
        if (
            local.status == OfferStatus.ACTIVE
            and local.keitaro_offer_id in keitaro_baseline_active
        ):
            local.status = OfferStatus.REMOVED
            local.is_pinned = False
            local.pinned_percent = None
            changed = True

    if changed:
        recalculate_stream_offers(list(offer_stream.offers))

    await _sync_service_streams(db, campaign, remote_streams)
    campaign.sync_status = SyncStatus.DRAFT
    db.commit()
    db.refresh(campaign)


async def _full_fetch_replace(
    db: Session,
    client: KeitaroClient,
    campaign: Campaign,
    remote_streams: list[dict],
) -> None:
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
            offer_name = await _refresh_offer_name(client, int(oid))
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
    db.flush()
    offer_streams = db.scalars(
        select(Stream).where(
            Stream.campaign_id == campaign.id,
            Stream.stream_type == StreamType.OFFER,
        ),
    ).all()
    for stream in offer_streams:
        save_stream_snapshot(db, stream)
    db.commit()
    db.refresh(campaign)


async def full_fetch(db: Session, client: KeitaroClient, campaign: Campaign) -> None:
    if campaign.keitaro_campaign_id is None:
        raise KeitaroError("У кампании нет Keitaro ID")

    remote_streams = await client.list_campaign_streams(campaign.keitaro_campaign_id)
    loaded = load_campaign_for_editor(db, campaign.id) or campaign

    offer_stream: Stream | None = None
    for stream in loaded.streams or []:
        if stream.stream_type == StreamType.OFFER:
            offer_stream = stream
            break

    if offer_stream is not None and offer_stream.has_draft:
        await _merge_fetch_preserve_draft(db, client, loaded, offer_stream, remote_streams)
        return

    await _full_fetch_replace(db, client, loaded, remote_streams)