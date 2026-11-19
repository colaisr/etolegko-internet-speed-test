"""Часто используемые ISO-3166-1 alpha-2 для создателя (подсказки UI; валидация — любой ISO-2)."""

from typing import TypedDict


class GeoPreset(TypedDict):
    code: str
    name: str


# Порядок: частые в арбитраже, затем по алфавиту кода.
_GEO_RAW: list[tuple[str, str]] = [
    ("AU", "Австралия"),
    ("US", "США"),
    ("GB", "Великобритания"),
    ("DE", "Германия"),
    ("FR", "Франция"),
    ("IT", "Италия"),
    ("ES", "Испания"),
    ("PL", "Польша"),
    ("BR", "Бразилия"),
    ("MX", "Мексика"),
    ("PE", "Перу"),
    ("CO", "Колумбия"),
    ("CL", "Чили"),
    ("AR", "Аргентина"),
    ("ID", "Индонезия"),
    ("TH", "Таиланд"),
    ("VN", "Вьетнам"),
    ("PH", "Филиппины"),
    ("IN", "Индия"),
    ("MY", "Малайзия"),
    ("KZ", "Казахстан"),
    ("UZ", "Узбекистан"),
    ("RU", "Россия"),
    ("UA", "Украина"),
    ("RO", "Румыния"),
    ("TR", "Турция"),
    ("SA", "Саудовская Аравия"),
    ("AE", "ОАЭ"),
    ("ZA", "ЮАР"),
    ("CA", "Канада"),
    ("NZ", "Новая Зеландия"),
    ("NL", "Нидерланды"),
    ("BE", "Бельгия"),
    ("AT", "Австрия"),
    ("CH", "Швейцария"),
    ("SE", "Швеция"),
    ("NO", "Норвегия"),
    ("FI", "Финляндия"),
    ("DK", "Дания"),
    ("PT", "Португалия"),
    ("GR", "Греция"),
    ("CZ", "Чехия"),
    ("HU", "Венгрия"),
    ("SK", "Словакия"),
    ("BG", "Болгария"),
    ("RS", "Сербия"),
    ("HR", "Хорватия"),
    ("IL", "Израиль"),
    ("EG", "Египет"),
    ("NG", "Нигерия"),
    ("KE", "Кения"),
    ("JP", "Япония"),
    ("KR", "Корея"),
    ("TW", "Тайвань"),
    ("SG", "Сингапур"),
    ("HK", "Гонконг"),
]

GEO_PRESETS: list[GeoPreset] = [{"code": code, "name": name} for code, name in _GEO_RAW]

# Быстрый выбор на форме
GEO_QUICK_PICKS: tuple[str, ...] = ("AU", "US", "GB", "DE", "PE", "BR", "MX", "KZ", "TH", "ID")


def filter_geo_presets(query: str, *, limit: int = 20) -> list[GeoPreset]:
    q = query.strip().lower()
    if not q:
        return GEO_PRESETS
    out: list[GeoPreset] = []
    for row in GEO_PRESETS:
        code = row["code"].lower()
        name = row["name"].lower()
        if code.startswith(q) or q in name or (len(q) == 1 and code.startswith(q)):
            out.append(row)
        if len(out) >= limit:
            break
    return out