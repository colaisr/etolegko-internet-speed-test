from legko.services.offer_search import filter_offers

SAMPLE = [
    {"id": 18813, "name": "Flexacil PE"},
    {"id": 42, "name": "Other"},
]


def test_filter_offers_by_name():
    assert filter_offers(SAMPLE, "flex")[0]["id"] == 18813


def test_filter_offers_empty_returns_top():
    assert len(filter_offers(SAMPLE, "")) == 2