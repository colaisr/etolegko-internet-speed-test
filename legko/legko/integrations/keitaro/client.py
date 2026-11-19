import secrets
import string
from dataclasses import dataclass

import httpx

from legko.settings import Settings


def _random_campaign_alias(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def campaign_url_from_keitaro(data: dict) -> str | None:
    domain = (data.get("domain") or "").rstrip("/")
    alias = (data.get("alias") or "").strip()
    if domain and alias:
        return f"{domain}/{alias}"
    for key in ("url", "campaign_url"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


class KeitaroError(Exception):
    def __init__(self, user_message: str, *, status_code: int | None = None) -> None:
        super().__init__(user_message)
        self.user_message = user_message
        self.status_code = status_code


@dataclass(frozen=True)
class PingResult:
    ok: bool
    message: str


class KeitaroClient:
    def __init__(self, settings: Settings, *, timeout: float = 15.0) -> None:
        self._base_url = settings.keitaro_base_url.rstrip("/")
        self._api_key = settings.keitaro_api_key
        self._timeout = timeout

    def _headers(self) -> dict[str, str]:
        return {"Api-Key": self._api_key, "Accept": "application/json"}

    async def ping(self) -> PingResult:
        if not self._api_key.strip():
            return PingResult(ok=False, message="Keitaro: не задан KEITARO_API_KEY")
        url = f"{self._base_url}/campaigns"
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(
                    url,
                    headers=self._headers(),
                    params={"limit": 1},
                )
        except httpx.TimeoutException:
            return PingResult(ok=False, message="Keitaro: таймаут соединения")
        except httpx.RequestError:
            return PingResult(ok=False, message="Keitaro: ошибка сети")

        if response.status_code in (401, 403):
            return PingResult(ok=False, message="Keitaro: неверный API key или доступ запрещён")
        if response.status_code >= 400:
            return PingResult(
                ok=False,
                message=f"Keitaro: HTTP {response.status_code}",
            )
        return PingResult(ok=True, message="ok")

    async def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        if not self._api_key.strip():
            raise KeitaroError("Не задан KEITARO_API_KEY")
        url = f"{self._base_url}/{path.lstrip('/')}"
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                return await client.request(method, url, headers=self._headers(), **kwargs)
        except httpx.TimeoutException as exc:
            raise KeitaroError("Keitaro: таймаут соединения") from exc
        except httpx.RequestError as exc:
            raise KeitaroError("Keitaro: ошибка сети") from exc

    @staticmethod
    def _response_error(response: httpx.Response) -> str:
        try:
            data = response.json()
            if isinstance(data, dict):
                for key in ("message", "error", "errors"):
                    val = data.get(key)
                    if isinstance(val, str) and val.strip():
                        return val.strip()
                    if isinstance(val, list) and val:
                        return str(val[0])
        except (ValueError, TypeError):
            pass
        return f"Keitaro: HTTP {response.status_code}"

    async def _request_checked(self, method: str, path: str, **kwargs) -> httpx.Response:
        response = await self._request(method, path, **kwargs)
        if response.status_code in (401, 403):
            raise KeitaroError("Keitaro: неверный API key или доступ запрещён")
        if response.status_code >= 400:
            raise KeitaroError(self._response_error(response), status_code=response.status_code)
        return response

    async def get_campaign(self, campaign_id: int) -> dict | None:
        response = await self._request("GET", f"campaigns/{campaign_id}")
        if response.status_code == 404:
            return None
        if response.status_code in (401, 403):
            raise KeitaroError("Keitaro: неверный API key или доступ запрещён")
        if response.status_code >= 400:
            raise KeitaroError(f"Keitaro: HTTP {response.status_code}")
        data = response.json()
        if isinstance(data, list):
            return data[0] if data else None
        if isinstance(data, dict) and "rows" in data:
            rows = data.get("rows") or []
            return rows[0] if rows else None
        return data if isinstance(data, dict) else None

    async def list_campaigns(self, *, limit: int = 100) -> list[dict]:
        response = await self._request("GET", "campaigns", params={"limit": limit})
        if response.status_code in (401, 403):
            raise KeitaroError("Keitaro: неверный API key или доступ запрещён")
        if response.status_code >= 400:
            raise KeitaroError(f"Keitaro: HTTP {response.status_code}")
        data = response.json()
        if isinstance(data, list):
            return [row for row in data if isinstance(row, dict)]
        if isinstance(data, dict):
            rows = data.get("rows") or data.get("data")
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
        return []

    async def list_offers(self, *, limit: int = 200) -> list[dict]:
        response = await self._request_checked("GET", "offers", params={"limit": limit})
        data = response.json()
        if isinstance(data, list):
            return [row for row in data if isinstance(row, dict)]
        return []

    async def get_offer(self, offer_id: int) -> dict | None:
        response = await self._request("GET", f"offers/{offer_id}")
        if response.status_code == 404:
            return None
        if response.status_code >= 400:
            raise KeitaroError(self._response_error(response), status_code=response.status_code)
        data = response.json()
        return data if isinstance(data, dict) else None

    async def delete_campaign(self, campaign_id: int) -> None:
        response = await self._request("DELETE", f"campaigns/{campaign_id}")
        if response.status_code in (401, 403):
            raise KeitaroError("Keitaro: неверный API key или доступ запрещён")
        if response.status_code >= 400 and response.status_code != 404:
            raise KeitaroError(self._response_error(response), status_code=response.status_code)

    async def list_campaign_streams(self, campaign_id: int) -> list[dict]:
        response = await self._request_checked("GET", f"campaigns/{campaign_id}/streams")
        data = response.json()
        if isinstance(data, list):
            return [row for row in data if isinstance(row, dict)]
        return []

    async def create_campaign_with_template(
        self,
        *,
        name: str,
        geo: str,
        offer_id: int,
        group_id: int,
        domain_id: int,
        traffic_source_id: int,
        google_redirect_url: str,
    ) -> dict:
        """Create campaign + geo Google stream + default offer stream. Roll back campaign on stream failure."""
        campaign_body = {
            "name": name,
            "alias": _random_campaign_alias(),
            "group_id": group_id,
            "domain_id": domain_id,
            "traffic_source_id": traffic_source_id,
        }
        campaign_response = await self._request_checked(
            "POST",
            "campaigns",
            json=campaign_body,
        )
        created = campaign_response.json()
        if not isinstance(created, dict) or created.get("id") is None:
            raise KeitaroError("Keitaro: неожиданный ответ при создании кампании")
        campaign_id = int(created["id"])

        geo_stream = {
            "name": f"Geo {geo}",
            "campaign_id": campaign_id,
            "type": "regular",
            "schema": "redirect",
            "action_type": "http",
            "action_payload": google_redirect_url,
            "filters": [{"name": "country", "mode": "accept", "payload": [geo]}],
            "offers": [],
            "landings": [],
        }
        offer_stream = {
            "name": "Offers",
            "campaign_id": campaign_id,
            "type": "default",
            "schema": "landings",
            "action_type": "http",
            "action_payload": "",
            "filters": [],
            "offers": [{"offer_id": offer_id, "share": 100, "state": "active"}],
            "landings": [],
        }

        try:
            await self._request_checked("POST", "streams", json=geo_stream)
            await self._request_checked("POST", "streams", json=offer_stream)
        except KeitaroError:
            await self.delete_campaign(campaign_id)
            raise

        refreshed = await self.get_campaign(campaign_id)
        if refreshed is None:
            raise KeitaroError("Keitaro: кампания создана, но не читается")
        return refreshed