from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from legko.db.session import get_db
from legko.services.health import build_health_report
from legko.settings import get_settings

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="Legko", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/health")
async def health(db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    report = await build_health_report(db, get_settings())
    code = 200 if report["status"] == "ok" else 503
    return JSONResponse(content=report, status_code=code)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"page_title": "Главная"},
    )