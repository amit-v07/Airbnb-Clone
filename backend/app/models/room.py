"""Room ORM model."""

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ARRAY, Boolean, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import RoomType

if TYPE_CHECKING:
    from app.models.hotel import Hotel
    from app.models.booking import Booking
    from app.models.inventory import RoomInventory


class Room(Base):
    """A room within a hotel that can be booked."""

    __tablename__ = "rooms"

    # ── Foreign Key ───────────────────────────────────────────────────────────
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("hotels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Room Details ──────────────────────────────────────────────────────────
    room_number: Mapped[str] = mapped_column(String(20), nullable=False)
    room_type: Mapped[RoomType] = mapped_column(
        Enum(RoomType, name="room_type_enum"), nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── Capacity & Pricing ────────────────────────────────────────────────────
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    base_price_per_night: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )

    # ── Amenities & Media ─────────────────────────────────────────────────────
    amenities: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    images: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Relationships ─────────────────────────────────────────────────────────
    hotel: Mapped["Hotel"] = relationship("Hotel", back_populates="rooms")
    bookings: Mapped[List["Booking"]] = relationship(
        "Booking", back_populates="room", lazy="select"
    )
    inventory: Mapped[List["RoomInventory"]] = relationship(
        "RoomInventory", back_populates="room", cascade="all, delete-orphan"
    )
