import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from legko.db.session import get_db
from legko.integrations.keitaro.client import KeitaroClient, KeitaroError
from legko.services.editor_view import editor_context, load_campaign_for_editor
from legko.services.stream_fetch import full_fetch
from legko.services.campaign_nav import (
    OpenCampaignError,
    get_campaign_or_404,
    list_recent_campaigns,
    open_by_keitaro_id,
    parse_keitaro_id,
    sync_status_badge_class,
    sync_status_label,
    sync_status_pill_class,
)
from legko.domain.geo_presets import GEO_PRESETS, GEO_QUICK_PICKS, filter_geo_presets
from legko.services.campaign_creator import (
    CreatorConfigError,
    CreatorValidationError,
    create_campaign_from_form,
    creator_config_view,
    get_created_campaign,
    parse_offer_id,
    success_context,
)
from legko.services.offer_editor import (
    OfferEditorError,
    add_offer,
    remove_offer,
    restore_offer,
    set_pin,
)
from legko.services.campaign_search import search_keitaro_campaigns
from legko.services.offer_search import search_keitaro_offers
from legko.settings import get_settings

router = APIRouter()


def _templates(request: Request):
    return request.app.state.templates


def _is_htmx(request: Request) -> bool:
    return request.headers.get("HX-Request") == "true"


def _creator_form_context(
    *,
    error_message: str | None = None,
    form_name: str = "",
    form_geo: str = "",
    form_offer_id: str = "",
    form_offer_label: str = "",
) -> dict:
    settings = get_settings()
    cfg = creator_config_view(settings)
    return {
        "error_message": error_message,
        "form_name": form_name,
        "form_geo": form_geo,
        "form_offer_id": form_offer_id,
        "form_offer_label": form_offer_label,
        "geo_presets": GEO_PRESETS,
        "geo_quick_picks": GEO_QUICK_PICKS,
        **cfg,
    }


async def _build_success_context(
    db: Session,
    campaign_id: uuid.UUID,
) -> dict | None:
    settings = get_settings()
    campaign = get_created_campaign(db, campaign_id)
    if campaign is None or campaign.keitaro_campaign_id is None:
        return None

    client = KeitaroClient(settings)
    offer_row = None
    for stream in campaign.streams:
        if stream.offers:
            offer_row = stream.offers[0]
            break
    if offer_row is not None:
        offer_id = offer_row.keitaro_offer_id
        offer_name = offer_row.offer_name or campaign.name
        if not offer_row.offer_name:
            try:
                remote_offer = await client.get_offer(offer_id)
                if remote_offer:
                    offer_name = (remote_offer.get("name") or f"Offer #{offer_id}")[:512]
            except Exception:
                offer_name = f"Offer #{offer_id}"
    else:
        offer_id = 0
        offer_name = "—"
        try:
            streams = await client.list_campaign_streams(campaign.keitaro_campaign_id)
            for remote in streams:
                offers = remote.get("offers") or []
                if offers:
                    offer_id = int(offers[0].get("offer_id") or 0)
                    offer_name = f"Offer #{offer_id}"
                    break
        except Exception:
            pass

    return success_context(
        campaign,
        settings,
        offer_id=offer_id,
        offer_name=offer_name,
    )


def _short_traffic_label(url: str | None) -> str | None:
    if not url or not url.strip():
        return None
    text = url.strip().replace("https://", "").replace("http://", "")
    if len(text) > 36:
        return f"{text[:33]}…"
    return text


def _format_updated_at(campaign) -> str:
    updated = getattr(campaign, "updated_at", None)
    if updated is None:
        return "—"
    try:
        return updated.strftime("%d.%m · %H:%M")
    except (TypeError, ValueError):
        return "—"


def _recent_view(db: Session) -> list[dict]:
    items = []
    for c in list_recent_campaigns(db):
        items.append(
            {
                "id": c.id,
                "name": c.name or f"Кампания #{c.keitaro_campaign_id}",
                "keitaro_campaign_id": c.keitaro_campaign_id,
                "geo_code": c.geo_code or "—",
                "traffic_label": _short_traffic_label(c.campaign_url),
                "updated_label": _format_updated_at(c),
                "badge_label": sync_status_label(c.sync_status),
                "badge_class": sync_status_badge_class(c.sync_status),
                "pill_class": sync_status_pill_class(c.sync_status),
            },
        )
    return items


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    error: str | None = None,
    create: int | None = None,
    created: uuid.UUID | None = None,
) -> HTMLResponse:
    created_panel_url = f"/campaigns/{created}/created/panel" if created else None
    return _templates(request).TemplateResponse(
        request=request,
        name="home.html",
        context={
            "page_title": "Главная",
            "nav_home": True,
            "recent": _recent_view(db),
            "error_message": error,
            "open_create_modal": create == 1,
            "created_panel_url": created_panel_url,
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


@router.get("/geo/search", response_class=HTMLResponse)
async def geo_search(
    request: Request,
    q: str = "",
) -> HTMLResponse:
    items = filter_geo_presets(q)
    return _templates(request).TemplateResponse(
        request=request,
        name="partials/geo_search_results.html",
        context={"items": items, "query": q.strip()},
    )


@router.get("/offers/search", response_class=HTMLResponse)
async def offer_search(
    request: Request,
    q: str = "",
) -> HTMLResponse:
    settings = get_settings()
    client = KeitaroClient(settings)
    items, keitaro_total = await search_keitaro_offers(client, q)
    return _templates(request).TemplateResponse(
        request=request,
        name="partials/offer_search_results.html",
        context={
            "items": items,
            "query": q.strip(),
            "keitaro_offer_total": keitaro_total,
        },
    )


@router.get("/campaigns/new/panel", response_class=HTMLResponse)
async def creator_form_panel(
    request: Request,
    error: str | None = None,
) -> HTMLResponse:
    return _templates(request).TemplateResponse(
        request=request,
        name="partials/creator_form_panel.html",
        context=_creator_form_context(error_message=error),
    )


@router.get("/campaigns/new", response_class=HTMLResponse)
async def creator_form(
    request: Request,
    error: str | None = None,
) -> RedirectResponse:
    from urllib.parse import quote

    url = "/?create=1"
    if error:
        url += f"&error={quote(error)}"
    return RedirectResponse(url=url, status_code=303)


@router.get("/campaigns/{campaign_id}/recent/panel", response_class=HTMLResponse)
async def campaign_recent_panel(
    request: Request,
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    campaign = get_campaign_or_404(db, campaign_id)
    if campaign is None:
        return _templates(request).TemplateResponse(
            request=request,
            name="partials/creator_form_panel.html",
            context=_creator_form_context(error_message="Кампания не найдена"),
            status_code=404,
        )
    return _templates(request).TemplateResponse(
        request=request,
        name="partials/campaign_recent_panel.html",
        context={
            "local_id": campaign.id,
            "campaign_name": campaign.name or f"Кампания #{campaign.keitaro_campaign_id}",
            "keitaro_campaign_id": campaign.keitaro_campaign_id,
            "badge_label": sync_status_label(campaign.sync_status),
            "badge_class": sync_status_badge_class(campaign.sync_status),
            "pill_class": sync_status_pill_class(campaign.sync_status),
        },
    )


@router.get("/campaigns/open/panel", response_class=HTMLResponse)
async def campaign_open_panel(
    request: Request,
    keitaro_campaign_id: str = "",
    name: str = "",
) -> HTMLResponse:
    try:
        kid = parse_keitaro_id(keitaro_campaign_id)
    except OpenCampaignError:
        kid = 0
    return _templates(request).TemplateResponse(
        request=request,
        name="partials/campaign_open_panel.html",
        context={
            "keitaro_campaign_id": kid,
            "campaign_name": name.strip() or f"Campaign #{keitaro_campaign_id}",
        },
    )


@router.post("/campaigns/new")
async def creator_submit(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    name: Annotated[str, Form()] = "",
    geo: Annotated[str, Form()] = "",
    offer_id: Annotated[str, Form()] = "",
):
    settings = get_settings()
    client = KeitaroClient(settings)

    try:
        campaign = await create_campaign_from_form(
            db,
            client,
            settings,
            name=name,
            geo_raw=geo,
            offer_id_raw=offer_id,
        )
    except (CreatorValidationError, CreatorConfigError) as exc:
        offer_label = ""
        if offer_id.strip():
            try:
                oid = parse_offer_id(offer_id)
                offer_label = f"#{oid}"
            except CreatorValidationError:
                offer_label = offer_id
        ctx = _creator_form_context(
            error_message=exc.user_message,
            form_name=name,
            form_geo=geo,
            form_offer_id=offer_id,
            form_offer_label=offer_label,
        )
        if _is_htmx(request):
            return _templates(request).TemplateResponse(
                request=request,
                name="partials/creator_form_panel.html",
                context=ctx,
                status_code=400,
            )
        return _templates(request).TemplateResponse(
            request=request,
            name="creator.html",
            context={"page_title": "Новая кампания", "nav_create": True, **ctx},
            status_code=400,
        )

    if _is_htmx(request):
        success_ctx = await _build_success_context(db, campaign.id)
        if success_ctx is None:
            return _templates(request).TemplateResponse(
                request=request,
                name="partials/creator_form_panel.html",
                context=_creator_form_context(error_message="Кампания не найдена после create"),
                status_code=500,
            )
        response = _templates(request).TemplateResponse(
            request=request,
            name="partials/creator_success_panel.html",
            context=success_ctx,
        )
        response.headers["HX-Trigger"] = "legkoRecentRefresh"
        return response

    return RedirectResponse(
        url=f"/?created={campaign.id}",
        status_code=303,
    )


@router.get("/campaigns/{campaign_id}/created/panel", response_class=HTMLResponse)
async def creator_success_panel(
    request: Request,
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
):
    ctx = await _build_success_context(db, campaign_id)
    if ctx is None:
        return _templates(request).TemplateResponse(
            request=request,
            name="partials/creator_form_panel.html",
            context=_creator_form_context(error_message="Кампания не найдена"),
            status_code=404,
        )
    return _templates(request).TemplateResponse(
        request=request,
        name="partials/creator_success_panel.html",
        context=ctx,
    )


@router.get("/campaigns/{campaign_id}/created", response_class=HTMLResponse)
async def creator_success(
    request: Request,
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
):
    return RedirectResponse(url=f"/?created={campaign_id}", status_code=303)


@router.get("/partials/recent-campaigns", response_class=HTMLResponse)
async def recent_campaigns_partial(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    return _templates(request).TemplateResponse(
        request=request,
        name="partials/recent_campaigns.html",
        context={"recent": _recent_view(db)},
    )


def _editor_template_context(
    campaign,
    *,
    fetch_error: str | None = None,
    op_error: str | None = None,
) -> dict:
    ctx = editor_context(campaign)
    return {
        "page_title": campaign.name,
        "nav_home": False,
        "badge_label": sync_status_label(campaign.sync_status),
        "pill_class": sync_status_pill_class(campaign.sync_status),
        "fetch_error": fetch_error,
        "op_error": op_error,
        **ctx,
    }


def _editor_redirect(campaign_id: uuid.UUID, *, op_error: str | None = None) -> RedirectResponse:
    from urllib.parse import quote

    base = f"/campaigns/{campaign_id}/editor"
    if op_error:
        return RedirectResponse(url=f"{base}?op_error={quote(op_error, safe='')}", status_code=303)
    return RedirectResponse(url=base, status_code=303)


@router.get("/campaigns/{campaign_id}/editor", response_class=HTMLResponse)
async def editor_page(
    request: Request,
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    fetch_error: str | None = None,
    op_error: str | None = None,
):
    campaign = load_campaign_for_editor(db, campaign_id)
    if campaign is None:
        return RedirectResponse(url="/?error=Кампания+не+найдена", status_code=303)
    return _templates(request).TemplateResponse(
        request=request,
        name="editor.html",
        context=_editor_template_context(campaign, fetch_error=fetch_error, op_error=op_error),
    )


@router.post("/campaigns/{campaign_id}/fetch", response_class=RedirectResponse)
async def campaign_fetch_streams(
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
):
    from urllib.parse import quote

    campaign = load_campaign_for_editor(db, campaign_id)
    if campaign is None:
        return RedirectResponse(url="/?error=Кампания+не+найдена", status_code=303)
    settings = get_settings()
    client = KeitaroClient(settings)
    try:
        await full_fetch(db, client, campaign)
    except KeitaroError as exc:
        msg = quote(exc.user_message, safe="")
        return RedirectResponse(
            url=f"/campaigns/{campaign_id}/editor?fetch_error={msg}",
            status_code=303,
        )
    return RedirectResponse(url=f"/campaigns/{campaign_id}/editor", status_code=303)


@router.post("/campaigns/{campaign_id}/offers", response_class=RedirectResponse)
async def editor_add_offer(
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    offer_id: Annotated[str, Form()] = "",
):
    settings = get_settings()
    client = KeitaroClient(settings)
    try:
        oid = parse_offer_id(offer_id)
        await add_offer(db, client, campaign_id, keitaro_offer_id=oid)
    except (CreatorValidationError, OfferEditorError, KeitaroError) as exc:
        msg = getattr(exc, "user_message", str(exc))
        return _editor_redirect(campaign_id, op_error=msg)
    return _editor_redirect(campaign_id)


@router.post("/campaigns/{campaign_id}/offers/{offer_row_id}/remove", response_class=RedirectResponse)
async def editor_remove_offer_row(
    campaign_id: uuid.UUID,
    offer_row_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
):
    try:
        remove_offer(db, campaign_id, offer_row_id)
    except OfferEditorError as exc:
        return _editor_redirect(campaign_id, op_error=exc.user_message)
    return _editor_redirect(campaign_id)


@router.post("/campaigns/{campaign_id}/offers/{offer_row_id}/restore", response_class=RedirectResponse)
async def editor_restore_offer_row(
    campaign_id: uuid.UUID,
    offer_row_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
):
    try:
        restore_offer(db, campaign_id, offer_row_id)
    except OfferEditorError as exc:
        return _editor_redirect(campaign_id, op_error=exc.user_message)
    return _editor_redirect(campaign_id)


@router.post("/campaigns/{campaign_id}/offers/{offer_row_id}/pin", response_class=RedirectResponse)
async def editor_pin_offer_row(
    campaign_id: uuid.UUID,
    offer_row_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    pin_percent: Annotated[str, Form()] = "",
):
    percent: int | None = None
    if pin_percent.strip():
        try:
            percent = int(pin_percent.strip())
        except ValueError:
            return _editor_redirect(campaign_id, op_error="Pin % должен быть числом")
    try:
        set_pin(db, campaign_id, offer_row_id, enabled=True, percent=percent)
    except OfferEditorError as exc:
        return _editor_redirect(campaign_id, op_error=exc.user_message)
    return _editor_redirect(campaign_id)


@router.post("/campaigns/{campaign_id}/offers/{offer_row_id}/unpin", response_class=RedirectResponse)
async def editor_unpin_offer_row(
    campaign_id: uuid.UUID,
    offer_row_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
):
    try:
        set_pin(db, campaign_id, offer_row_id, enabled=False)
    except OfferEditorError as exc:
        return _editor_redirect(campaign_id, op_error=exc.user_message)
    return _editor_redirect(campaign_id)


@router.get("/docs", response_class=HTMLResponse)
async def docs_stub(request: Request) -> HTMLResponse:
    return _templates(request).TemplateResponse(
        request=request,
        name="docs_stub.html",
        context={"page_title": "Документация"},
    )