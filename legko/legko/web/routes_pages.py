import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from legko.db.session import get_db
from legko.integrations.keitaro.client import KeitaroClient
from legko.services.campaign_nav import (
    OpenCampaignError,
    get_campaign_or_404,
    list_recent_campaigns,
    open_by_keitaro_id,
    parse_keitaro_id,
    sync_status_badge_class,
    sync_status_label,
)
from legko.services.campaign_search import search_keitaro_campaigns
from legko.settings import get_settings

router = APIRouter()


def _templates(request: Request):
    return request.app.state.templates


def _recent_view(db: Session) -> list[dict]:
    items = []
    for c in list_recent_campaigns(db):
        items.append(
            {
                "id": c.id,
                "name": c.name or f"Кампания #{c.keitaro_campaign_id}",
                "keitaro_campaign_id": c.keitaro_campaign_id,
                "badge_label": sync_status_label(c.sync_status),
                "badge_class": sync_status_badge_class(c.sync_status),
            },
        )
    return items


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    error: str | None = None,
) -> HTMLResponse:
    return _templates(request).TemplateResponse(
        request=request,
        name="home.html",
        context={
            "page_title": "Главная",
            "nav_home": True,
            "recent": _recent_view(db),
            "error_message": error,
        },
    )


@router.get("/campaigns/search", response_class=HTMLResponse)
async def campaign_search(
    request: Request,
    q: str = "",
) -> HTMLResponse:
    settings = get_settings()
    client = KeitaroClient(settings)
    items = await search_keitaro_campaigns(client, q)
    return _templates(request).TemplateResponse(
        request=request,
        name="partials/campaign_search_results.html",
        context={"items": items, "query": q.strip()},
    )


@router.post("/campaigns/open")
async def open_campaign_post(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    keitaro_campaign_id: Annotated[str, Form()] = "",
    q: Annotated[str, Form()] = "",
) -> RedirectResponse:
    settings = get_settings()
    client = KeitaroClient(settings)
    raw_id = keitaro_campaign_id.strip() or q.strip()
    try:
        kid = parse_keitaro_id(raw_id)
        local_id = await open_by_keitaro_id(db, client, kid)
    except OpenCampaignError as exc:
        from urllib.parse import quote

        return RedirectResponse(url=f"/?error={quote(exc.user_message)}", status_code=303)
    return RedirectResponse(url=f"/campaigns/{local_id}/editor", status_code=303)


@router.get("/campaigns/new", response_class=HTMLResponse)
async def creator_stub(request: Request) -> HTMLResponse:
    return _templates(request).TemplateResponse(
        request=request,
        name="creator_stub.html",
        context={"page_title": "Новая кампания", "nav_create": True},
    )


@router.get("/campaigns/{campaign_id}/editor", response_class=HTMLResponse)
async def editor_stub(
    request: Request,
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
):
    campaign = get_campaign_or_404(db, campaign_id)
    if campaign is None:
        return RedirectResponse(url="/?error=Кампания+не+найдена", status_code=303)
    return _templates(request).TemplateResponse(
        request=request,
        name="editor_stub.html",
        context={
            "page_title": campaign.name,
            "nav_editor": True,
            "campaign": campaign,
            "badge_label": sync_status_label(campaign.sync_status),
            "badge_class": sync_status_badge_class(campaign.sync_status),
        },
    )


@router.get("/docs", response_class=HTMLResponse)
async def docs_stub(request: Request) -> HTMLResponse:
    return _templates(request).TemplateResponse(
        request=request,
        name="docs_stub.html",
        context={"page_title": "Документация"},
    )