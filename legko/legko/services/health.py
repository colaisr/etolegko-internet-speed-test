from sqlalchemy import text
from sqlalchemy.orm import Session

from legko.integrations.keitaro import KeitaroClient
from legko.settings import Settings


def check_database(db: Session) -> tuple[bool, str]:
    try:
        db.execute(text("SELECT 1"))
        return True, "ok"
    except Exception:  # noqa: BLE001
        return False, "database: ошибка подключения"


async def build_health_report(db: Session, settings: Settings) -> dict:
    db_ok, db_msg = check_database(db)
    client = KeitaroClient(settings)
    ping = await client.ping()
    keitaro_ok = ping.ok
    overall = db_ok and keitaro_ok
    return {
        "status": "ok" if overall else "degraded",
        "app": {"ok": True, "message": "ok"},
        "database": {"ok": db_ok, "message": db_msg},
        "keitaro": {"ok": keitaro_ok, "message": ping.message},
    }