"""Распределение целых процентов (largest remainder / Hamilton) между active офферами."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeightInput:
    """Один слот для пересчёта."""

    key: str
    active: bool
    pinned: bool
    pinned_percent: int | None
    current_percent: int = 0


class WeightRecalcError(ValueError):
    pass


def distribute_total_among_equal_slots(count: int, total: int) -> list[int]:
    """Делит total на count целых долей; сумма ровно total (Hamilton при равных долях)."""
    if count <= 0:
        if total != 0:
            raise WeightRecalcError("Некуда распределить вес")
        return []
    if total < 0:
        raise WeightRecalcError("Отрицательный остаток веса")
    base = total // count
    extra = total % count
    return [base + (1 if i < extra else 0) for i in range(count)]


def recalculate_weights(slots: list[WeightInput]) -> dict[str, int]:
    """
    Возвращает map key -> weight_percent.
    Неактивные (removed) → 0.
  """
    result: dict[str, int] = {}
    active = [s for s in slots if s.active]

    pinned_weights: dict[str, int] = {}
    pinned_sum = 0
    for slot in active:
        if slot.pinned:
            pct = slot.pinned_percent if slot.pinned_percent is not None else slot.current_percent
            if pct < 0 or pct > 100:
                raise WeightRecalcError("Некорректный pin %")
            pinned_weights[slot.key] = pct
            pinned_sum += pct

    if pinned_sum > 100:
        raise WeightRecalcError("Сумма закреплённых весов больше 100%")

    unpinned = [s for s in active if not s.pinned]
    remaining = 100 - pinned_sum
    unpinned_weights = distribute_total_among_equal_slots(len(unpinned), remaining)

    for slot in slots:
        if not slot.active:
            result[slot.key] = 0
        elif slot.pinned:
            result[slot.key] = pinned_weights[slot.key]
        else:
            idx = unpinned.index(slot)
            result[slot.key] = unpinned_weights[idx]

    if sum(result[k] for k in result if any(s.key == k and s.active for s in slots)) != 100:
        active_sum = sum(result[s.key] for s in active)
        if active and active_sum != 100:
            raise WeightRecalcError("Сумма active должна быть 100%")

    return result