import uuid

from sqlalchemy.orm import Session

from legko.domain.weights import WeightInput, WeightRecalcError, recalculate_weights
from legko.integrations.keitaro.client import KeitaroClient
from legko.models import Campaign, OfferStatus, Stream, StreamOffer, StreamType, SyncStatus
from legko.services.editor_view import load_campaign_for_editor


class OfferEditorError(Exception):
    def __init__(self, message: str) -> None:
        self.user_message = message
        super().__init__(message)


def _offer_stream(campaign: Campaign) -> Stream:
    for stream in campaign.streams or []:
        if stream.stream_type == StreamType.OFFER:
            return stream
    raise OfferEditorError("Оффер-поток не найден — сделайте Fetch Streams")


def _mark_draft(stream: Stream, campaign: Campaign) -> None:
    stream.has_draft = True
    campaign.sync_status = SyncStatus.DRAFT


def _inputs_from_offers(offers: list[StreamOffer]) -> list[WeightInput]:
    return [
        WeightInput(
            key=str(row.id),
            active=row.status == OfferStatus.ACTIVE,
            pinned=row.is_pinned,
            pinned_percent=row.pinned_percent,
            current_percent=row.weight_percent,
        )
        for row in offers
    ]


def apply_recalculated_weights(offers: list[StreamOffer], weights: dict[str, int]) -> None:
    for row in offers:
        row.weight_percent = weights.get(str(row.id), 0)


def recalculate_stream_offers(offers: list[StreamOffer]) -> None:
    try:
        weights = recalculate_weights(_inputs_from_offers(offers))
    except WeightRecalcError as exc:
        raise OfferEditorError(exc.args[0]) from exc
    apply_recalculated_weights(offers, weights)


def _find_by_keitaro_id(offers: list[StreamOffer], keitaro_offer_id: int) -> StreamOffer | None:
    for row in offers:
        if row.keitaro_offer_id == keitaro_offer_id:
            return row
    return None


async def add_offer(
    db: Session,
    client: KeitaroClient,
    campaign_id: uuid.UUID,
    *,
    keitaro_offer_id: int,
) -> None:
    campaign = load_campaign_for_editor(db, campaign_id)
    if campaign is None:
        raise OfferEditorError("Кампания не найдена")
    stream = _offer_stream(campaign)
    offers = list(stream.offers)

    existing = _find_by_keitaro_id(offers, keitaro_offer_id)
    if existing is not None:
        if existing.status == OfferStatus.ACTIVE:
            raise OfferEditorError("Оффер уже в ротации")
        existing.status = OfferStatus.ACTIVE
        existing.is_pinned = False
        existing.pinned_percent = None
    else:
        remote = await client.get_offer(keitaro_offer_id)
        if remote is None:
            raise OfferEditorError("Оффер не найден в Keitaro")
        name = (remote.get("name") or f"Offer #{keitaro_offer_id}")[:512]
        offers.append(
            StreamOffer(
                stream_id=stream.id,
                keitaro_offer_id=keitaro_offer_id,
                offer_name=name,
                weight_percent=0,
                status=OfferStatus.ACTIVE,
            ),
        )
        db.add(offers[-1])
        db.flush()

    recalculate_stream_offers(offers)
    _mark_draft(stream, campaign)
    db.commit()


def remove_offer(db: Session, campaign_id: uuid.UUID, offer_row_id: uuid.UUID) -> None:
    campaign = load_campaign_for_editor(db, campaign_id)
    if campaign is None:
        raise OfferEditorError("Кампания не найдена")
    stream = _offer_stream(campaign)
    row = db.get(StreamOffer, offer_row_id)
    if row is None or row.stream_id != stream.id:
        raise OfferEditorError("Строка оффера не найдена")
    if row.status == OfferStatus.REMOVED:
        raise OfferEditorError("Оффер уже удалён")
    row.status = OfferStatus.REMOVED
    row.is_pinned = False
    row.pinned_percent = None
    recalculate_stream_offers(list(stream.offers))
    _mark_draft(stream, campaign)
    db.commit()


def restore_offer(db: Session, campaign_id: uuid.UUID, offer_row_id: uuid.UUID) -> None:
    campaign = load_campaign_for_editor(db, campaign_id)
    if campaign is None:
        raise OfferEditorError("Кампания не найдена")
    stream = _offer_stream(campaign)
    row = db.get(StreamOffer, offer_row_id)
    if row is None or row.stream_id != stream.id:
        raise OfferEditorError("Строка оффера не найдена")
    if row.status != OfferStatus.REMOVED:
        raise OfferEditorError("Оффер не в статусе removed")
    row.status = OfferStatus.ACTIVE
    recalculate_stream_offers(list(stream.offers))
    _mark_draft(stream, campaign)
    db.commit()


def set_pin(
    db: Session,
    campaign_id: uuid.UUID,
    offer_row_id: uuid.UUID,
    *,
    enabled: bool,
    percent: int | None = None,
) -> None:
    campaign = load_campaign_for_editor(db, campaign_id)
    if campaign is None:
        raise OfferEditorError("Кампания не найдена")
    stream = _offer_stream(campaign)
    row = db.get(StreamOffer, offer_row_id)
    if row is None or row.stream_id != stream.id:
        raise OfferEditorError("Строка оффера не найдена")
    if row.status != OfferStatus.ACTIVE:
        raise OfferEditorError("Pin только для активных офферов")

    if enabled:
        pin_val = percent if percent is not None else row.weight_percent
        if pin_val < 0 or pin_val > 100:
            raise OfferEditorError("Pin % должен быть от 0 до 100")
        row.is_pinned = True
        row.pinned_percent = pin_val
        row.weight_percent = pin_val
    else:
        row.is_pinned = False
        row.pinned_percent = None

    recalculate_stream_offers(list(stream.offers))
    _mark_draft(stream, campaign)
    db.commit()