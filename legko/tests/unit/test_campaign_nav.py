import pytest

from legko.models import SyncStatus
from legko.services.campaign_nav import OpenCampaignError, parse_keitaro_id, sync_status_label


def test_parse_keitaro_id_valid():
    assert parse_keitaro_id(" 8812 ") == 8812


@pytest.mark.parametrize("raw", ["", "abc", "0", "-1", "12.3"])
def test_parse_keitaro_id_invalid(raw):
    with pytest.raises(OpenCampaignError):
        parse_keitaro_id(raw)


def test_sync_status_labels():
    assert sync_status_label(SyncStatus.SYNCED) == "Синхронно"
    assert sync_status_label(SyncStatus.DRAFT) == "Черновик"