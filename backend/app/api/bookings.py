"""Bookings API router — /bookings."""

import uuid
from typing import List

from fastapi import APIRouter

from app.dependencies import DBSession, CurrentUser, AdminUser
from app.schemas.booking import BookingCreate, BookingStatusUpdate, BookingResponse
from app.schemas.responses import APIResponse, MessageResponse
from app.schemas.payment import PaymentStatusResponse
from app.services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get(
    "",
    response_model=APIResponse[List[BookingResponse]],
    summary="Get all bookings for the current user",
)
async def list_bookings(current_user: CurrentUser, db: DBSession):
    """Return all bookings associated with the authenticated user."""
    service = BookingService(db)
    bookings = await service.get_user_bookings(current_user)
    return APIResponse(data=[BookingResponse.model_validate(b) for b in bookings])


@router.post(
    "",
    response_model=APIResponse[BookingResponse],
    status_code=201,
    summary="Create a new booking",
)
async def create_booking(
    payload: BookingCreate,
    current_user: CurrentUser,
    db: DBSession,
):
    """Create a booking for a room. Price is calculated dynamically."""
    service = BookingService(db)
    booking = await service.create_booking(payload, current_user)
    return APIResponse(
        message="Booking created successfully",
        data=BookingResponse.model_validate(booking),
    )


@router.get(
    "/{booking_id}",
    response_model=APIResponse[BookingResponse],
    summary="Get a booking by ID",
)
async def get_booking(
    booking_id: uuid.UUID,
    current_user: CurrentUser,
    db: DBSession,
):
    """Return a booking. Users can only fetch their own; admins can fetch any."""
    service = BookingService(db)
    booking = await service.get_by_id(booking_id, current_user)
    return APIResponse(data=BookingResponse.model_validate(booking))


@router.put(
    "/{booking_id}",
    response_model=APIResponse[BookingResponse],
    summary="Update booking status",
)
async def update_booking_status(
    booking_id: uuid.UUID,
    payload: BookingStatusUpdate,
    current_user: CurrentUser,
    db: DBSession,
):
    """Update the status of a booking (admin or owner)."""
    service = BookingService(db)
    booking = await service.update_status(booking_id, payload, current_user)
    return APIResponse(
        message="Booking status updated",
        data=BookingResponse.model_validate(booking),
    )


@router.delete(
    "/{booking_id}",
    response_model=MessageResponse,
    summary="Cancel a booking",
)
async def cancel_booking(
    booking_id: uuid.UUID,
    current_user: CurrentUser,
    db: DBSession,
):
    """Cancel a booking and release room inventory."""
    service = BookingService(db)
    await service.cancel_booking(booking_id, current_user)
    return MessageResponse(message="Booking cancelled successfully")


@router.get(
    "/{booking_id}/payment-status",
    response_model=APIResponse[PaymentStatusResponse],
    summary="Check payment status for a booking",
)
async def get_payment_status(
    booking_id: uuid.UUID,
    current_user: CurrentUser,
    db: DBSession,
):
    """Return the current payment status of a booking."""
    from app.services.checkout_service import CheckoutService
    service = CheckoutService(db)
    status = await service.get_payment_status(booking_id, current_user.id)
    return APIResponse(data=status)
