from legko.services.campaign_search import filter_campaigns

SAMPLE = [
    {"id": 215033, "name": "test_dushenko_flex123"},
    {"id": 99, "name": "other_campaign"},
]


def test_filter_by_id_prefix():
    assert filter_campaigns(SAMPLE, "215") == [{"id": 215033, "name": "test_dushenko_flex123"}]


def test_filter_by_name():
    result = filter_campaigns(SAMPLE, "dushenko")
    assert len(result) == 1
    assert result[0]["id"] == 215033


def test_filter_empty_returns_top():
    assert filter_campaigns(SAMPLE, "") == SAMPLE