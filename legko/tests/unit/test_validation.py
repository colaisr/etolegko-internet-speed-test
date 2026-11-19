from legko.domain.validation import push_readiness
from legko.models import OfferStatus, StreamOffer


def test_push_readiness_requires_active_and_hundred():
    bad = push_readiness([StreamOffer(keitaro_offer_id=1, weight_percent=40, status=OfferStatus.ACTIVE)])
    assert not bad.ok
    assert "100%" in (bad.reason or "")

    good = push_readiness(
        [
            StreamOffer(keitaro_offer_id=1, weight_percent=60, status=OfferStatus.ACTIVE),
            StreamOffer(keitaro_offer_id=2, weight_percent=40, status=OfferStatus.ACTIVE),
        ],
    )
    assert good.ok