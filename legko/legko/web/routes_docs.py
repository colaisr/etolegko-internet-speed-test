from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from legko.services.product_docs import (
    list_doc_pages,
    read_doc_file,
    read_index_markdown,
    resolve_doc_path,
)
from legko.web.doc_renderer import extract_title, render_product_doc_markdown

router = APIRouter()


def _templates(request: Request):
    return request.app.state.templates


@router.get("/docs", response_class=HTMLResponse)
async def docs_index(request: Request) -> HTMLResponse:
    pages = list_doc_pages()
    index_md = read_index_markdown()
    body_html = None
    if index_md:
        body_html = render_product_doc_markdown(index_md)
    return _templates(request).TemplateResponse(
        request=request,
        name="docs_index.html",
        context={
            "page_title": "Документация",
            "nav_home": False,
            "pages": pages,
            "index_html": body_html,
        },
    )


@router.get("/docs/{slug}", response_class=HTMLResponse)
async def docs_page(request: Request, slug: str) -> HTMLResponse:
    path = resolve_doc_path(slug)
    if path is None:
        return _templates(request).TemplateResponse(
            request=request,
            name="docs_not_found.html",
            context={
                "page_title": "Раздел не найден",
                "nav_home": False,
                "pages": list_doc_pages(),
                "slug": slug,
            },
            status_code=404,
        )
    source = read_doc_file(path)
    title = extract_title(source, fallback=slug)
    return _templates(request).TemplateResponse(
        request=request,
        name="docs_page.html",
        context={
            "page_title": title,
            "nav_home": False,
            "pages": list_doc_pages(),
            "slug": path.stem,
            "content_html": render_product_doc_markdown(source),
        },
    )


@router.get("/docs/", include_in_schema=False)
async def docs_trailing_slash() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=301)