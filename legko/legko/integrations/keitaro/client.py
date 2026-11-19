from dataclasses import dataclass

import httpx

from legko.settings import Settings


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