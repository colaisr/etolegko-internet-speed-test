import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON, Uuid

from legko.db.base import Base


class StreamPublishedSnapshot(Base):
    """Last synced offer rows for Cancel and push diff (F5/F6)."""

    __tablename__ = "stream_published_snapshots"

    stream_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("streams.id", ondelete="CASCADE"),
        primary_key=True,
    )
    payload: Mapped[list] = mapped_column(JSON, default=list)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    stream: Mapped["Stream"] = relationship(back_populates="published_snapshot")  # noqa: F821