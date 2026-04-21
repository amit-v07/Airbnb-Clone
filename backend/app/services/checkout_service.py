"""Checkout service — Stripe payment session creation and webhook handling."""

import uuid

import stripe
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.exceptions import NotFoundException, BadRequestException, PaymentException
from app.models.booking import Booking
from app.models.enums import BookingStatus, PaymentStatus
from app.schemas.payment import CheckoutRequest, CheckoutResponse, PaymentStatusResponse

stripe.api_key = settings.STRIPE_API_KEY


class CheckoutService:
    """Manages Stripe payment checkout sessions and webhook events."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_checkout_session(
        self, payload: CheckoutRequest, user_id: uuid.UUID
    ) -> CheckoutResponse:
        """Create a Stripe Checkout session for a pending booking.

        Raises:
            NotFoundException: if booking not found.
            BadRequestException: if booking doesn't belong to user or already paid.
            PaymentException: if Stripe call fails.
        """
        booking: Booking | None = await self.db.scalar(
            select(Booking).where(Booking.id == payload.booking_id)
        )
        if not booking:
            raise NotFoundException("Booking", str(payload.booking_id))

        if booking.user_id != user_id:
            raise BadRequestException("Booking does not belong to this user")

        if booking.payment_status == PaymentStatus.PAID:
            raise BadRequestException("Booking is already paid")

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"Booking #{str(booking.id)[:8].upper()}",
                                "description": (
                                    f"Check-in: {booking.check_in_date} — "
                                    f"Check-out: {booking.check_out_date}"
                                ),
                            },
                            "unit_amount": int(booking.total_price * 100),  # cents
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=payload.success_url,
                cancel_url=payload.cancel_url,
                metadata={"booking_id": str(booking.id)},
            )
        except stripe.StripeError as exc:
            raise PaymentException(f"Stripe error: {exc.user_message}") from exc

        # Store session reference
        booking.stripe_session_id = session.id
        await self.db.flush()

        return CheckoutResponse(checkout_url=session.url, session_id=session.id)

    async def handle_webhook(self, payload: bytes, sig_header: str) -> None:
        """Process incoming Stripe webhook events.

        Raises:
            BadRequestException: if the signature is invalid.
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.SignatureVerificationError) as exc:
            raise BadRequestException(f"Webhook verification failed: {exc}") from exc

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            booking_id = session.get("metadata", {}).get("booking_id")

            if booking_id:
                booking: Booking | None = await self.db.scalar(
                    select(Booking).where(Booking.id == uuid.UUID(booking_id))
                )
                if booking:
                    booking.payment_status = PaymentStatus.PAID
                    booking.status = BookingStatus.CONFIRMED
                    booking.stripe_payment_intent_id = session.get("payment_intent")
                    await self.db.flush()

    async def get_payment_status(
        self, booking_id: uuid.UUID, user_id: uuid.UUID
    ) -> PaymentStatusResponse:
        """Return the payment status of a booking."""
        booking: Booking | None = await self.db.scalar(
            select(Booking).where(Booking.id == booking_id)
        )
        if not booking:
            raise NotFoundException("Booking", str(booking_id))

        if booking.user_id != user_id:
            raise BadRequestException("Access denied")

        return PaymentStatusResponse(
            booking_id=booking.id,
            payment_status=booking.payment_status,
            stripe_payment_intent_id=booking.stripe_payment_intent_id,
        )
