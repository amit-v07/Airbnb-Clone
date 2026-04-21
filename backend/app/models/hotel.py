"""Hotel ORM model."""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ARRAY, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.room import Room


class Hotel(Base):
    """A hotel property listed on the platform."""

    __tablename__ = "hotels"

    # ── Basic Info ────────────────────────────────────────────────────────────
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(String(512), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # ── Location Coordinates ──────────────────────────────────────────────────
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # ── Media ─────────────────────────────────────────────────────────────────
    thumbnail: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    images: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)

    # ── Meta ──────────────────────────────────────────────────────────────────
    star_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    amenities: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)

    # ── Relationships ─────────────────────────────────────────────────────────
    rooms: Mapped[List["Room"]] = relationship(
        "Room", back_populates="hotel", lazy="select", cascade="all, delete-orphan"
    )
