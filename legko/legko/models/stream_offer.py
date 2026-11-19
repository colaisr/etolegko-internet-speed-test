import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from legko.db.base import Base


class OfferStatus(str, enum.Enum):
    ACTIVE = "active"
    REMOVED = "removed"


class StreamOffer(Base):
    __tablename__ = "stream_offers"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stream_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("streams.id", ondelete="CASCADE"),
    )
    keitaro_offer_id: Mapped[int] = mapped_column(Integer)
    offer_name: Mapped[str | None] = mapped_column(String(512), nullable=True)
    weight_percent: Mapped[int] = mapped_column(Integer, default=0)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    pinned_percent: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[OfferStatus] = mapped_column(
        Enum(OfferStatus, native_enum=False),
        default=OfferStatus.ACTIVE,
    )

    stream: Mapped["Stream"] = relationship(back_populates="offers")  # noqa: F821