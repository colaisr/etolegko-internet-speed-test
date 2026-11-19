import uuid

from sqlalchemy.orm import Session

from legko.models import OfferStatus, Stream, StreamOffer, StreamPublishedSnapshot, StreamType


def snapshot_rows_from_offers(offers: list[StreamOffer]) -> list[dict]:
    rows = [
        {
            "keitaro_offer_id": row.keitaro_offer_id,
            "offer_name": row.offer_name,
            "weight_percent": row.weight_percent,
            "status": row.status.value,
            "is_pinned": row.is_pinned,
            "pinned_percent": row.pinned_percent,
        }
        for row in offers
    ]
    rows.sort(key=lambda item: item["keitaro_offer_id"])
    return rows


def save_stream_snapshot(db: Session, stream: Stream) -> None:
    if stream.stream_type != StreamType.OFFER:
        return
    payload = snapshot_rows_from_offers(list(stream.offers or []))
    existing = db.get(StreamPublishedSnapshot, stream.id)
    if existing is None:
        db.add(StreamPublishedSnapshot(stream_id=stream.id, payload=payload))
    else:
        existing.payload = payload


def load_snapshot_payload(db: Session, stream_id: uuid.UUID) -> list[dict] | None:
    row = db.get(StreamPublishedSnapshot, stream_id)
    if row is None or not row.payload:
        return None
    return list(row.payload)


def restore_offers_from_snapshot(
    db: Session,
    stream: Stream,
    payload: list[dict],
) -> None:
    by_keitaro: dict[int, StreamOffer] = {
        row.keitaro_offer_id: row for row in stream.offers
    }
    seen: set[int] = set()
    for item in payload:
        kid = int(item["keitaro_offer_id"])
        seen.add(kid)
        status = OfferStatus(item.get("status", OfferStatus.ACTIVE.value))
        target = by_keitaro.get(kid)
        if target is None:
            target = StreamOffer(
                stream_id=stream.id,
                keitaro_offer_id=kid,
                offer_name=item.get("offer_name"),
                weight_percent=int(item.get("weight_percent") or 0),
                is_pinned=bool(item.get("is_pinned")),
                pinned_percent=item.get("pinned_percent"),
                status=status,
            )
            db.add(target)
            by_keitaro[kid] = target
        else:
            target.offer_name = item.get("offer_name")
            target.weight_percent = int(item.get("weight_percent") or 0)
            target.is_pinned = bool(item.get("is_pinned"))
            target.pinned_percent = item.get("pinned_percent")
            target.status = status

    for kid, row in list(by_keitaro.items()):
        if kid not in seen:
            db.delete(row)