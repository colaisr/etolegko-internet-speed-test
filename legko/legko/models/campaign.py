import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from legko.db.base import Base


class SyncStatus(str, enum.Enum):
    SYNCED = "synced"
    DRAFT = "draft"
    NEEDS_FETCH = "needs_fetch"


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    keitaro_campaign_id: Mapped[int | None] = mapped_column(unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), default="")
    campaign_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    geo_code: Mapped[str | None] = mapped_column(String(8), nullable=True)
    sync_status: Mapped[SyncStatus] = mapped_column(
        Enum(SyncStatus, native_enum=False),
        default=SyncStatus.NEEDS_FETCH,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    streams: Mapped[list["Stream"]] = relationship(back_populates="campaign")  # noqa: F821