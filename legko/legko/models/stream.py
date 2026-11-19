import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from legko.db.base import Base


class StreamType(str, enum.Enum):
    OFFER = "offer"
    SERVICE = "service"


class Stream(Base):
    __tablename__ = "streams"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
    )
    keitaro_stream_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    stream_type: Mapped[StreamType] = mapped_column(Enum(StreamType, native_enum=False))
    has_draft: Mapped[bool] = mapped_column(Boolean, default=False)

    campaign: Mapped["Campaign"] = relationship(back_populates="streams")  # noqa: F821
    offers: Mapped[list["StreamOffer"]] = relationship(back_populates="stream")  # noqa: F821