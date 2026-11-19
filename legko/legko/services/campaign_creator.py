import re
import uuid

from sqlalchemy.orm import Session

from legko.integrations.keitaro.client import (
    KeitaroClient,
    KeitaroError,
    campaign_url_from_keitaro,
)
from legko.models import Campaign, SyncStatus
from legko.services.stream_fetch import full_fetch
from legko.settings import Settings

_GEO_RE = re.compile(r"^[A-Z]{2}$")


class CreatorValidationError(Exception):
    def __init__(self, user_message: str) -> None:
        super().__init__(user_message)
        self.user_message = user_message


class CreatorConfigError(Exception):
    def __init__(self, user_message: str) -> None:
        super().__init__(user_message)
        self.user_message = user_message


def parse_creator_default_ids(settings: Settings) -> tuple[int, int, int]:
    parts = (
        settings.keitaro_default_domain_id.strip(),
        settings.keitaro_default_group_id.strip(),
        settings.keitaro_default_source_id.strip(),
    )
    if not all(parts):
        raise CreatorConfigError(
            "Задайте KEITARO_DEFAULT_DOMAIN_ID, GROUP_ID и SOURCE_ID в .env (см. README)",
        )
    try:
        domain_id, group_id, source_id = (int(p) for p in parts)
    except ValueError as exc:
        raise CreatorConfigError("ID домена, группы и источника должны быть целыми числами") from exc
    if min(domain_id, group_id, source_id) <= 0:
        raise CreatorConfigError("ID домена, группы и источника должны быть положительными")
    return domain_id, group_id, source_id


def normalize_geo(raw: str) -> str:
    geo = raw.strip().upper()
    if not _GEO_RE.fullmatch(geo):
        raise CreatorValidationError("Geo: укажите код страны ISO-2 (например, AU)")
    return geo


def parse_offer_id(raw: str) -> int:
    text = raw.strip()
    if not text or not re.fullmatch(r"\d+", text):
        raise CreatorValidationError("Выберите оффер из списка или введите числовой ID")
    value = int(text)
    if value <= 0:
        raise CreatorValidationError("Некорректный ID оффера")
    return value


def validate_campaign_name(raw: str) -> str:
    name = raw.strip()
    if not name:
        raise CreatorValidationError("Введите название кампании")
    if len(name) > 255:
        raise CreatorValidationError("Название длиннее 255 символов")
    return name


async def validate_offer_exists(client: KeitaroClient, offer_id: int) -> str:
    try:
        remote = await client.get_offer(offer_id)
    except KeitaroError as exc:
        raise CreatorValidationError(exc.user_message) from exc
    if remote is None:
        raise CreatorValidationError("Оффер не найден в Keitaro")
    return (remote.get("name") or f"Offer #{offer_id}")[:512]


def creator_config_view(settings: Settings) -> dict:
    try:
        domain_id, group_id, source_id = parse_creator_default_ids(settings)
        configured = True
        config_error = None
    except CreatorConfigError as exc:
        domain_id = group_id = source_id = None
        configured = False
        config_error = exc.user_message

    return {
        "configured": configured,
        "config_error": config_error,
        "domain_id": domain_id,
        "group_id": group_id,
        "source_id": source_id,
        "google_redirect_url": settings.keitaro_google_redirect_url,
    }


async def create_campaign_from_form(
    db: Session,
    client: KeitaroClient,
    settings: Settings,
    *,
    name: str,
    geo_raw: str,
    offer_id_raw: str,
) -> Campaign:
    domain_id, group_id, source_id = parse_creator_default_ids(settings)
    campaign_name = validate_campaign_name(name)
    geo = normalize_geo(geo_raw)
    offer_id = parse_offer_id(offer_id_raw)
    offer_name = await validate_offer_exists(client, offer_id)

    try:
        remote = await client.create_campaign_with_template(
            name=campaign_name,
            geo=geo,
            offer_id=offer_id,
            group_id=group_id,
            domain_id=domain_id,
            traffic_source_id=source_id,
            google_redirect_url=settings.keitaro_google_redirect_url,
        )
    except KeitaroError as exc:
        raise CreatorValidationError(exc.user_message) from exc

    keitaro_id = int(remote["id"])
    campaign = Campaign(
        keitaro_campaign_id=keitaro_id,
        name=campaign_name,
        campaign_url=campaign_url_from_keitaro(remote),
        geo_code=geo,
        sync_status=SyncStatus.NEEDS_FETCH,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    try:
        await full_fetch(db, client, campaign)
    except KeitaroError:
        campaign.sync_status = SyncStatus.NEEDS_FETCH
        db.commit()

    return campaign


def success_context(
    campaign: Campaign,
    settings: Settings,
    *,
    offer_id: int,
    offer_name: str,
) -> dict:
    cfg = creator_config_view(settings)
    return {
        "campaign": campaign,
        "offer_id": offer_id,
        "offer_name": offer_name,
        "domain_id": cfg["domain_id"],
        "group_id": cfg["group_id"],
        "source_id": cfg["source_id"],
        "google_redirect_url": cfg["google_redirect_url"],
    }


def get_created_campaign(db: Session, local_id: uuid.UUID) -> Campaign | None:
    return db.get(Campaign, local_id)