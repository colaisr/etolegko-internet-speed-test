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