"""Payment Pydantic schemas (DTOs)."""

import uuid
from typing import Optional

from pydantic import BaseModel

from app.models.enums import PaymentStatus


class CheckoutRequest(BaseModel):
    """Request to initiate a Stripe checkout session for a booking."""

    booking_id: uuid.UUID
    success_url: str
    cancel_url: str


class CheckoutResponse(BaseModel):
    """Stripe checkout session response."""

    checkout_url: str
    session_id: str


class PaymentStatusResponse(BaseModel):
    """Result of a payment status lookup."""

    booking_id: uuid.UUID
    payment_status: PaymentStatus
    stripe_payment_intent_id: Optional[str] = None
