from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from legko.db.session import get_db
from legko.services.health import build_health_report
from legko.settings import get_settings
from legko.web.routes_docs import router as docs_router
from legko.web.routes_pages import router as pages_router

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# /docs — зарезервировано под ProductDocs (F9); OpenAPI — отдельно.
app = FastAPI(title="Legko", version="0.1.0", docs_url="/api/docs", redoc_url="/api/redoc")
app.state.templates = templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(pages_router)
app.include_router(docs_router)


@app.get("/health")
async def health(db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    report = await build_health_report(db, get_settings())
    code = 200 if report["status"] == "ok" else 503
    return JSONResponse(content=report, status_code=code)
