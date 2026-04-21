"""Room Pydantic schemas (DTOs)."""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.enums import RoomType


# ── Base ──────────────────────────────────────────────────────────────────────
class RoomBase(BaseModel):
    room_number: str = Field(..., min_length=1, max_length=20)
    room_type: RoomType
    description: Optional[str] = None
    capacity: int = Field(2, ge=1, le=20)
    base_price_per_night: Decimal = Field(..., gt=0)
    amenities: Optional[List[str]] = None
    is_available: bool = True


# ── Request Schemas ───────────────────────────────────────────────────────────
class RoomCreate(RoomBase):
    """Schema for creating a room under a hotel."""

    images: Optional[List[str]] = None


class RoomUpdate(BaseModel):
    """Partial update schema for a room."""

    room_number: Optional[str] = Field(None, min_length=1, max_length=20)
    room_type: Optional[RoomType] = None
    description: Optional[str] = None
    capacity: Optional[int] = Field(None, ge=1, le=20)
    base_price_per_night: Optional[Decimal] = Field(None, gt=0)
    amenities: Optional[List[str]] = None
    images: Optional[List[str]] = None
    is_available: Optional[bool] = None


# ── Response Schemas ──────────────────────────────────────────────────────────
class RoomResponse(RoomBase):
    """Room data returned by the API."""

    model_config = {"from_attributes": True}

    id: uuid.UUID
    hotel_id: uuid.UUID
    images: Optional[List[str]] = None
    created_at: datetime


class RoomWithPriceResponse(RoomResponse):
    """Room response with dynamically calculated price."""

    calculated_price: Optional[Decimal] = None
