"""Room inventory ORM model — tracks availability per date."""

import uuid
from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.room import Room


class RoomInventory(Base):
    """Tracks room availability on a per-date basis.

    Each row represents one calendar day for one room.
    is_available=False means the room is booked for that date.
    """

    __tablename__ = "room_inventory"

    # ── Foreign Key ───────────────────────────────────────────────────────────
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Date & Availability ───────────────────────────────────────────────────
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    reserved_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Relationship ──────────────────────────────────────────────────────────
    room: Mapped["Room"] = relationship("Room", back_populates="inventory")
