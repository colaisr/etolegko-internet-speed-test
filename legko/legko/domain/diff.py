from dataclasses import dataclass, field

from legko.models import OfferStatus


@dataclass
class PushDiff:
    adds: list[dict] = field(default_factory=list)
    removes: list[dict] = field(default_factory=list)
    weight_changes: list[dict] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not self.adds and not self.removes and not self.weight_changes


def _active_by_id(snapshot_rows: list[dict]) -> dict[int, dict]:
    out: dict[int, dict] = {}
    for row in snapshot_rows:
        if row.get("status") != OfferStatus.ACTIVE.value:
            continue
        kid = row.get("keitaro_offer_id")
        if kid is not None:
            out[int(kid)] = row
    return out


def _active_current(offers) -> dict[int, object]:
    out = {}
    for row in offers:
        if row.status != OfferStatus.ACTIVE:
            continue
        out[row.keitaro_offer_id] = row
    return out


def build_push_diff(snapshot_rows: list[dict], current_offers) -> PushDiff:
    """Compare published snapshot rows to current stream offers for the push modal."""
    diff = PushDiff()
    baseline = _active_by_id(snapshot_rows)
    current = _active_current(current_offers)

    for kid, row in current.items():
        if kid not in baseline:
            diff.adds.append(
                {
                    "keitaro_offer_id": kid,
                    "offer_name": row.offer_name or f"Offer #{kid}",
                    "weight_percent": row.weight_percent,
                },
            )

    for kid, snap in baseline.items():
        if kid not in current:
            diff.removes.append(
                {
                    "keitaro_offer_id": kid,
                    "offer_name": snap.get("offer_name") or f"Offer #{kid}",
                    "weight_percent": int(snap.get("weight_percent") or 0),
                },
            )

    for kid, row in current.items():
        snap = baseline.get(kid)
        if snap is None:
            continue
        before = int(snap.get("weight_percent") or 0)
        after = row.weight_percent
        if before != after:
            diff.weight_changes.append(
                {
                    "keitaro_offer_id": kid,
                    "offer_name": row.offer_name or f"Offer #{kid}",
                    "before": before,
                    "after": after,
                },
            )

    diff.adds.sort(key=lambda item: item["keitaro_offer_id"])
    diff.removes.sort(key=lambda item: item["keitaro_offer_id"])
    diff.weight_changes.sort(key=lambda item: item["keitaro_offer_id"])
    return diff