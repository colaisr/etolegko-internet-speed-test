from legko.integrations.keitaro.client import KeitaroClient, KeitaroError


def filter_offers(offers: list[dict], query: str, *, limit: int = 15) -> list[dict]:
    q = query.strip().lower()
    if not q:
        return offers[:limit]

    out: list[dict] = []
    for row in offers:
        oid = row.get("id")
        name = (row.get("name") or "").lower()
        oid_str = str(oid) if oid is not None else ""
        if q.isdigit():
            if oid_str.startswith(q) or oid_str == q:
                out.append(row)
        elif q in name or q in oid_str:
            out.append(row)
        if len(out) >= limit:
            break
    return out


async def search_keitaro_offers(client: KeitaroClient, query: str) -> tuple[list[dict], int]:
    try:
        offers = await client.list_offers(limit=500)
    except KeitaroError:
        return [], 0
    normalized = [
        {
            "id": o.get("id"),
            "name": (o.get("name") or f"Offer #{o.get('id')}")[:120],
        }
        for o in offers
        if o.get("id") is not None
    ]
    return filter_offers(normalized, query), len(normalized)