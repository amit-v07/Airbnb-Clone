"""Payments API router — /payments/checkout, /payments/webhook."""

from fastapi import APIRouter, Header, Request

from app.dependencies import DBSession, CurrentUser
from app.schemas.payment import CheckoutRequest, CheckoutResponse
from app.schemas.responses import APIResponse, MessageResponse
from app.services.checkout_service import CheckoutService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post(
    "/checkout",
    response_model=APIResponse[CheckoutResponse],
    summary="Initiate a Stripe checkout session for a booking",
)
async def initiate_checkout(
    payload: CheckoutRequest,
    current_user: CurrentUser,
    db: DBSession,
):
    """Create a Stripe Checkout session and return the redirect URL."""
    service = CheckoutService(db)
    result = await service.create_checkout_session(payload, current_user.id)
    return APIResponse(
        message="Checkout session created",
        data=result,
    )


@router.post(
    "/webhook",
    response_model=MessageResponse,
    summary="Handle Stripe webhook events",
    include_in_schema=False,  # Don't expose in Swagger (internal)
)
async def stripe_webhook(
    request: Request,
    db: DBSession,
    stripe_signature: str = Header(None, alias="stripe-signature"),
):
    """
    Stripe webhook endpoint. Verifies and processes checkout.session.completed events.
    This endpoint must be registered in your Stripe dashboard.
    """
    payload = await request.body()
    service = CheckoutService(db)
    await service.handle_webhook(payload, stripe_signature or "")
    return MessageResponse(message="Webhook processed")
