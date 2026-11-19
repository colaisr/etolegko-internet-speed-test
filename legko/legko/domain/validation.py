from dataclasses import dataclass

from legko.models import OfferStatus, StreamOffer


@dataclass(frozen=True)
class PushReadiness:
    ok: bool
    reason: str | None = None


def active_offers(offers: list[StreamOffer]) -> list[StreamOffer]:
    return [row for row in offers if row.status == OfferStatus.ACTIVE]


def push_readiness(offers: list[StreamOffer]) -> PushReadiness:
    active = active_offers(offers)
    if not active:
        return PushReadiness(False, "Нет активных офферов")
    total = sum(row.weight_percent for row in active)
    if total != 100:
        return PushReadiness(False, f"Сумма весов: {total}% (нужно 100%)")
    return PushReadiness(True, None)