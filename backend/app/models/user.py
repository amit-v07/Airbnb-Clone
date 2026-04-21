"""User ORM model."""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import Gender, Role

if TYPE_CHECKING:
    from app.models.booking import Booking


class User(Base):
    """Registered user of the platform."""

    __tablename__ = "users"

    # ── Identity ─────────────────────────────────────────────────────────────
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # ── Profile ──────────────────────────────────────────────────────────────
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    profile_picture: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    gender: Mapped[Optional[Gender]] = mapped_column(
        Enum(Gender, name="gender_enum"), nullable=True
    )

    # ── Access Control ────────────────────────────────────────────────────────
    role: Mapped[Role] = mapped_column(
        Enum(Role, name="role_enum"),
        default=Role.USER,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Relationships ─────────────────────────────────────────────────────────
    bookings: Mapped[List["Booking"]] = relationship(
        "Booking", back_populates="user", lazy="select"
    )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
