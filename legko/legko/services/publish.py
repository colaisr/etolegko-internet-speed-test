import uuid

from sqlalchemy.orm import Session

from legko.domain.diff import PushDiff, build_push_diff
from legko.domain.validation import push_readiness
from legko.integrations.keitaro.client import KeitaroClient, KeitaroError
from legko.models import Campaign, OfferStatus, Stream, StreamType, SyncStatus
from legko.services.editor_view import load_campaign_for_editor
from legko.services.stream_snapshot import (
    load_snapshot_payload,
    restore_offers_from_snapshot,
    save_stream_snapshot,
)


class PublishError(Exception):
    def __init__(self, message: str) -> None:
        self.user_message = message
        super().__init__(message)


def _offer_stream(campaign: Campaign) -> Stream:
    for stream in campaign.streams or []:
        if stream.stream_type == StreamType.OFFER:
            return stream
    raise PublishError("Оффер-поток не найден — сделайте Fetch Streams")


def push_preview(db: Session, campaign_id: uuid.UUID) -> tuple[Campaign, PushDiff]:
    campaign = load_campaign_for_editor(db, campaign_id)
    if campaign is None:
        raise PublishError("Кампания не найдена")
    stream = _offer_stream(campaign)
    if not stream.has_draft:
        raise PublishError("Нет изменений для Push")
    readiness = push_readiness(list(stream.offers))
    if not readiness.ok:
        raise PublishError(readiness.reason or "Push недоступен")
    snapshot = load_snapshot_payload(db, stream.id)
    if snapshot is None:
        raise PublishError("Нет опорного снимка — обновите потоки из Keitaro")
    diff = build_push_diff(snapshot, list(stream.offers))
    return campaign, diff


async def push_to_keitaro(
    db: Session,
    client: KeitaroClient,
    campaign_id: uuid.UUID,
) -> None:
    campaign = load_campaign_for_editor(db, campaign_id)
    if campaign is None:
        raise PublishError("Кампания не найдена")
    stream = _offer_stream(campaign)
    if stream.keitaro_stream_id is None:
        raise PublishError("У потока нет Keitaro stream id")
    if not stream.has_draft:
        raise PublishError("Нет изменений для Push")

    offers = list(stream.offers)
    readiness = push_readiness(offers)
    if not readiness.ok:
        raise PublishError(readiness.reason or "Push недоступен")

    active = [
        (row.keitaro_offer_id, row.weight_percent)
        for row in offers
        if row.status == OfferStatus.ACTIVE
    ]
    if not active:
        raise PublishError("Нет активных офферов")

    try:
        await client.update_stream_offers(int(stream.keitaro_stream_id), active)
    except KeitaroError as exc:
        raise PublishError(exc.user_message) from exc

    save_stream_snapshot(db, stream)
    stream.has_draft = False
    campaign.sync_status = SyncStatus.SYNCED
    db.commit()


def cancel_draft(db: Session, campaign_id: uuid.UUID) -> None:
    campaign = load_campaign_for_editor(db, campaign_id)
    if campaign is None:
        raise PublishError("Кампания не найдена")
    stream = _offer_stream(campaign)
    if not stream.has_draft:
        raise PublishError("Нет черновика для отмены")
    payload = load_snapshot_payload(db, stream.id)
    if payload is None:
        raise PublishError("Нет опорного снимка — обновите потоки из Keitaro")

    restore_offers_from_snapshot(db, stream, payload)
    stream.has_draft = False
    campaign.sync_status = SyncStatus.SYNCED
    db.commit()