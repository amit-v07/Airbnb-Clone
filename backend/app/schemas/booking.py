"""Booking Pydantic schemas (DTOs)."""

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, model_validator

from app.models.enums import BookingStatus, PaymentStatus


# ── Guest Info Sub-Schema ─────────────────────────────────────────────────────
class GuestInfo(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    id_type: Optional[str] = Field(None, max_length=50)
    id_number: Optional[str] = Field(None, max_length=100)


# ── Request Schemas ───────────────────────────────────────────────────────────
class BookingCreate(BaseModel):
    """Schema for creating a new booking."""

    room_id: uuid.UUID
    check_in_date: date
    check_out_date: date
    guest: GuestInfo
    special_requests: Optional[str] = Field(None, max_length=1000)

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingCreate":
        if self.check_in_date >= self.check_out_date:
            raise ValueError("check_out_date must be after check_in_date")
        if self.check_in_date < date.today():
            raise ValueError("check_in_date cannot be in the past")
        return self


class BookingStatusUpdate(BaseModel):
    """Schema for updating booking status."""

    status: BookingStatus


# ── Response Schemas ──────────────────────────────────────────────────────────
class GuestResponse(GuestInfo):
    """Guest data returned with booking."""

    model_config = {"from_attributes": True}

    id: uuid.UUID


class BookingResponse(BaseModel):
    """Booking data returned by the API."""

    model_config = {"from_attributes": True}

    id: uuid.UUID
    user_id: Optional[uuid.UUID]
    room_id: uuid.UUID
    check_in_date: date
    check_out_date: date
    total_price: Decimal
    status: BookingStatus
    payment_status: PaymentStatus
    special_requests: Optional[str]
    stripe_session_id: Optional[str]
    guest: Optional[GuestResponse]
    created_at: datetime
