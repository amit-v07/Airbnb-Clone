"""Hotel Pydantic schemas (DTOs)."""

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ── Base ──────────────────────────────────────────────────────────────────────
class HotelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    address: str = Field(..., min_length=1, max_length=512)
    city: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    star_rating: Optional[int] = Field(None, ge=1, le=5)
    amenities: Optional[List[str]] = None


# ── Request Schemas ───────────────────────────────────────────────────────────
class HotelCreate(HotelBase):
    """Schema for creating a new hotel."""

    thumbnail: Optional[str] = None
    images: Optional[List[str]] = None


class HotelUpdate(BaseModel):
    """Schema for partial hotel update (all optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    star_rating: Optional[int] = Field(None, ge=1, le=5)
    amenities: Optional[List[str]] = None
    thumbnail: Optional[str] = None
    images: Optional[List[str]] = None


# ── Filter Schema ─────────────────────────────────────────────────────────────
class HotelSearchFilter(BaseModel):
    """Query parameters for browsing/filtering hotels."""

    city: Optional[str] = None
    country: Optional[str] = None
    min_rating: Optional[int] = Field(None, ge=1, le=5)
    max_rating: Optional[int] = Field(None, ge=1, le=5)
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


# ── Response Schemas ──────────────────────────────────────────────────────────
class HotelResponse(HotelBase):
    """Hotel data returned by the API."""

    model_config = {"from_attributes": True}

    id: uuid.UUID
    thumbnail: Optional[str] = None
    images: Optional[List[str]] = None
    created_at: datetime
