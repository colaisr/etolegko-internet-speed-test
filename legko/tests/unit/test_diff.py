from legko.domain.diff import build_push_diff
from legko.models import OfferStatus, StreamOffer


def _row(kid: int, weight: int, status=OfferStatus.ACTIVE, name: str | None = None):
    return StreamOffer(
        keitaro_offer_id=kid,
        offer_name=name or f"O{kid}",
        weight_percent=weight,
        status=status,
    )


def test_push_diff_add_remove_and_weights():
    snapshot = [
        {
            "keitaro_offer_id": 1,
            "offer_name": "A",
            "weight_percent": 50,
            "status": OfferStatus.ACTIVE.value,
        },
        {
            "keitaro_offer_id": 2,
            "offer_name": "B",
            "weight_percent": 50,
            "status": OfferStatus.ACTIVE.value,
        },
    ]
    current = [
        _row(1, 40),
        _row(3, 60),
    ]
    diff = build_push_diff(snapshot, current)
    assert len(diff.removes) == 1
    assert diff.removes[0]["keitaro_offer_id"] == 2
    assert len(diff.adds) == 1
    assert diff.adds[0]["keitaro_offer_id"] == 3
    assert len(diff.weight_changes) == 1
    assert diff.weight_changes[0]["before"] == 50
    assert diff.weight_changes[0]["after"] == 40