import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from legko.models import Campaign, OfferStatus, Stream, StreamType


def load_campaign_for_editor(db: Session, local_id: uuid.UUID) -> Campaign | None:
    stmt = (
        select(Campaign)
        .where(Campaign.id == local_id)
        .options(selectinload(Campaign.streams).selectinload(Stream.offers))
    )
    return db.scalars(stmt).first()


def _pick_stream(streams: list[Stream], stream_type: StreamType) -> Stream | None:
    for stream in streams:
        if stream.stream_type == stream_type:
            return stream
    return None


def editor_context(campaign: Campaign) -> dict:
    streams = list(campaign.streams or [])
    service_stream = _pick_stream(streams, StreamType.SERVICE)
    offer_stream = _pick_stream(streams, StreamType.OFFER)
    offers = []
    if offer_stream is not None:
        offers = sorted(
            offer_stream.offers,
            key=lambda row: (
                0 if row.status == OfferStatus.ACTIVE else 1,
                -row.weight_percent,
                row.keitaro_offer_id,
            ),
        )

    active_count = sum(1 for row in offers if row.status == OfferStatus.ACTIVE)
    active_sum = sum(
        row.weight_percent for row in offers if row.status == OfferStatus.ACTIVE
    )
    geo = (campaign.geo_code or "…").upper()
    weights_valid = active_sum == 100 and active_count > 0
    offer_stream_draft = bool(offer_stream and offer_stream.has_draft)
    can_push = offer_stream_draft and weights_valid
    can_cancel = offer_stream_draft

    push_disabled_reason: str | None = None
    if not offer_stream_draft:
        push_disabled_reason = "Нет изменений"
    elif not weights_valid:
        if active_count == 0:
            push_disabled_reason = "Нет активных офферов"
        else:
            push_disabled_reason = f"Сумма весов: {active_sum}% (нужно 100%)"

    return {
        "campaign": campaign,
        "service_stream": service_stream,
        "offer_stream": offer_stream,
        "offers": offers,
        "has_streams": bool(streams),
        "needs_fetch_cta": not streams,
        "offer_stream_draft": offer_stream_draft,
        "active_weight_sum": active_sum,
        "active_offer_count": active_count,
        "weights_valid": weights_valid,
        "can_push": can_push,
        "can_cancel": can_cancel,
        "push_disabled_reason": push_disabled_reason,
        "service_stream_label": f"Служебный поток ({geo} → Google)",
    }