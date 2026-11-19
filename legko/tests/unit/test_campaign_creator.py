from unittest.mock import AsyncMock, patch

import pytest
from starlette.testclient import TestClient

from legko.db.base import Base
from legko.db.session import engine
from legko.integrations.keitaro.client import KeitaroError
from legko.main import app
from legko.services.campaign_creator import (
    CreatorConfigError,
    CreatorValidationError,
    normalize_geo,
    parse_creator_default_ids,
    validate_campaign_name,
)
from legko.settings import Settings


def test_normalize_geo_valid():
    assert normalize_geo(" au ") == "AU"


@pytest.mark.parametrize("raw", ["", "A", "AUS", "12", "a1"])
def test_normalize_geo_invalid(raw):
    with pytest.raises(CreatorValidationError):
        normalize_geo(raw)


def test_validate_campaign_name():
    assert validate_campaign_name("  My camp  ") == "My camp"
    with pytest.raises(CreatorValidationError):
        validate_campaign_name("   ")


def test_parse_creator_default_ids_missing():
    settings = Settings(
        _env_file=None,
        KEITARO_DEFAULT_DOMAIN_ID="",
        KEITARO_DEFAULT_GROUP_ID="1",
        KEITARO_DEFAULT_SOURCE_ID="2",
    )
    with pytest.raises(CreatorConfigError):
        parse_creator_default_ids(settings)


def test_parse_creator_default_ids_ok():
    settings = Settings(
        _env_file=None,
        KEITARO_DEFAULT_DOMAIN_ID="1813",
        KEITARO_DEFAULT_GROUP_ID="10464",
        KEITARO_DEFAULT_SOURCE_ID="836",
    )
    assert parse_creator_default_ids(settings) == (1813, 10464, 836)


def test_creator_form_requires_config():
    Base.metadata.create_all(bind=engine)
    with (
        TestClient(app) as client,
        patch("legko.web.routes_pages.get_settings") as mock_settings,
    ):
        mock_settings.return_value = Settings(
            _env_file=None,
            KEITARO_API_KEY="test",
            KEITARO_DEFAULT_DOMAIN_ID="",
            KEITARO_DEFAULT_GROUP_ID="",
            KEITARO_DEFAULT_SOURCE_ID="",
        )
        response = client.get("/campaigns/new/panel")
    assert response.status_code == 200
    assert "KEITARO_DEFAULT" in response.text
    assert "disabled" in response.text


def test_creator_post_invalid_geo():
    Base.metadata.create_all(bind=engine)
    with (
        TestClient(app) as client,
        patch("legko.web.routes_pages.get_settings") as mock_settings,
        patch("legko.web.routes_pages.KeitaroClient") as mock_cls,
    ):
        mock_settings.return_value = Settings(
            _env_file=None,
            KEITARO_API_KEY="test",
            KEITARO_DEFAULT_DOMAIN_ID="1813",
            KEITARO_DEFAULT_GROUP_ID="10464",
            KEITARO_DEFAULT_SOURCE_ID="836",
        )
        mock_cls.return_value.get_offer = AsyncMock(return_value={"id": 1, "name": "Test"})
        mock_cls.return_value.create_campaign_with_template = AsyncMock()
        response = client.post(
            "/campaigns/new",
            data={"name": "X", "geo": "INVALID", "offer_id": "18813"},
        )
    assert response.status_code == 400
    mock_cls.return_value.create_campaign_with_template.assert_not_called()


def test_create_campaign_rollback_on_stream_error():
    import asyncio

    from legko.integrations.keitaro.client import KeitaroClient

    settings = Settings(
        _env_file=None,
        KEITARO_API_KEY="k",
        KEITARO_BASE_URL="https://example.test/admin_api/v1",
    )
    client = KeitaroClient(settings)

    campaign_payload = {
        "id": 99,
        "alias": "abc",
        "domain": "https://track.test/",
        "name": "T",
    }

    async def run() -> None:
        with patch.object(client, "_request_checked", new_callable=AsyncMock) as checked:
            checked.side_effect = [
                _mock_response(200, campaign_payload),
                KeitaroError("stream failed"),
            ]
            with patch.object(client, "delete_campaign", new_callable=AsyncMock) as delete_mock:
                with patch.object(
                    client,
                    "get_campaign",
                    new_callable=AsyncMock,
                    return_value=campaign_payload,
                ):
                    with pytest.raises(KeitaroError):
                        await client.create_campaign_with_template(
                            name="T",
                            geo="AU",
                            offer_id=1,
                            group_id=1,
                            domain_id=1,
                            traffic_source_id=1,
                            google_redirect_url="https://www.google.com",
                        )
                delete_mock.assert_awaited_once_with(99)

    asyncio.run(run())


def _mock_response(status: int, json_data: dict):
    from unittest.mock import MagicMock

    response = MagicMock()
    response.status_code = status
    response.json = MagicMock(return_value=json_data)
    return response