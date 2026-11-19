from legko.integrations.keitaro.client import KeitaroClient, KeitaroError


def filter_campaigns(campaigns: list[dict], query: str, *, limit: int = 12) -> list[dict]:
    q = query.strip().lower()
    if not q:
        return campaigns[:limit]

    out: list[dict] = []
    for row in campaigns:
        cid = row.get("id")
        name = (row.get("name") or "").lower()
        cid_str = str(cid) if cid is not None else ""
        if q.isdigit():
            if cid_str.startswith(q) or cid_str == q:
                out.append(row)
        elif q in name or q in cid_str:
            out.append(row)
        if len(out) >= limit:
            break
    return out


async def search_keitaro_campaigns(client: KeitaroClient, query: str) -> list[dict]:
    try:
        campaigns = await client.list_campaigns(limit=150)
    except KeitaroError:
        return []
    normalized = [
        {"id": c.get("id"), "name": (c.get("name") or f"Campaign #{c.get('id')}")[:120]}
        for c in campaigns
        if c.get("id") is not None
    ]
    return filter_campaigns(normalized, query)