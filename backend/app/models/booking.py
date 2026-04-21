"""Booking ORM model."""

import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import BookingStatus, PaymentStatus

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.room import Room
    from app.models.guest import Guest


class Booking(Base):
    """A reservation linking a User to a Room for specific dates."""

    __tablename__ = "bookings"

    # ── Foreign Keys ──────────────────────────────────────────────────────────
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Dates ─────────────────────────────────────────────────────────────────
    check_in_date: Mapped[date] = mapped_column(Date, nullable=False)
    check_out_date: Mapped[date] = mapped_column(Date, nullable=False)

    # ── Financial ─────────────────────────────────────────────────────────────
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # ── Status ────────────────────────────────────────────────────────────────
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, name="booking_status_enum"),
        default=BookingStatus.PENDING,
        nullable=False,
    )
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status_enum"),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    # ── Stripe Reference ──────────────────────────────────────────────────────
    stripe_payment_intent_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    stripe_session_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )

    # ── Special Requests ──────────────────────────────────────────────────────
    special_requests: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    # ── Relationships ─────────────────────────────────────────────────────────
    user: Mapped[Optional["User"]] = relationship("User", back_populates="bookings")
    room: Mapped["Room"] = relationship("Room", back_populates="bookings")
    guest: Mapped[Optional["Guest"]] = relationship(
        "Guest", back_populates="booking", uselist=False, cascade="all, delete-orphan"
    )
