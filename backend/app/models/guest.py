"""Guest ORM model — primary contact for a booking."""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking


class Guest(Base):
    """The primary guest information associated with a booking."""

    __tablename__ = "guests"

    # ── Foreign Key ───────────────────────────────────────────────────────────
    booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # ── Guest Identity ────────────────────────────────────────────────────────
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # ── ID Document ───────────────────────────────────────────────────────────
    id_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    id_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # ── Relationship ──────────────────────────────────────────────────────────
    booking: Mapped["Booking"] = relationship("Booking", back_populates="guest")
