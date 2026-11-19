import re
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from legko.integrations.keitaro.client import KeitaroClient, KeitaroError
from legko.models import Campaign, SyncStatus


class OpenCampaignError(Exception):
    def __init__(self, user_message: str) -> None:
        super().__init__(user_message)
        self.user_message = user_message


def list_recent_campaigns(db: Session, *, limit: int = 10) -> list[Campaign]:
    stmt = (
        select(Campaign)
        .where(Campaign.keitaro_campaign_id.isnot(None))
        .order_by(Campaign.updated_at.desc())
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


def parse_keitaro_id(raw: str) -> int:
    text = raw.strip()
    if not text or not re.fullmatch(r"\d+", text):
        raise OpenCampaignError("Введите числовой ID кампании Keitaro")
    value = int(text)
    if value <= 0:
        raise OpenCampaignError("Введите числовой ID кампании Keitaro")
    return value


async def open_by_keitaro_id(db: Session, client: KeitaroClient, keitaro_id: int) -> uuid.UUID:
    existing = db.scalar(
        select(Campaign).where(Campaign.keitaro_campaign_id == keitaro_id),
    )
    if existing:
        return existing.id

    try:
        remote = await client.get_campaign(keitaro_id)
    except KeitaroError as exc:
        raise OpenCampaignError(exc.user_message) from exc

    if remote is None:
        raise OpenCampaignError("Кампания не найдена")

    campaign = Campaign(
        keitaro_campaign_id=keitaro_id,
        name=(remote.get("name") or f"Campaign #{keitaro_id}")[:255],
        campaign_url=remote.get("url") or remote.get("campaign_url"),
        sync_status=SyncStatus.NEEDS_FETCH,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign.id


def get_campaign_or_404(db: Session, local_id: uuid.UUID) -> Campaign | None:
    return db.get(Campaign, local_id)


def sync_status_label(status: SyncStatus) -> str:
    return {
        SyncStatus.SYNCED: "Синхронно",
        SyncStatus.DRAFT: "Черновик",
        SyncStatus.NEEDS_FETCH: "Проверьте Keitaro",
    }.get(status, str(status.value))


def sync_status_badge_class(status: SyncStatus) -> str:
    return {
        SyncStatus.SYNCED: "badge-sync",
        SyncStatus.DRAFT: "badge-draft",
        SyncStatus.NEEDS_FETCH: "badge-needs-fetch",
    }.get(status, "badge-draft")


def sync_status_pill_class(status: SyncStatus) -> str:
    return {
        SyncStatus.SYNCED: "status-pill--sync",
        SyncStatus.DRAFT: "status-pill--draft",
        SyncStatus.NEEDS_FETCH: "status-pill--attention",
    }.get(status, "status-pill--draft")