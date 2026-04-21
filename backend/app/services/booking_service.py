"""Booking service — availability check, create, update, cancel."""

import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundException, ForbiddenException, RoomNotAvailableException
from app.models.booking import Booking
from app.models.guest import Guest
from app.models.room import Room
from app.models.user import User
from app.models.enums import BookingStatus
from app.schemas.booking import BookingCreate, BookingStatusUpdate
from app.services.inventory_service import InventoryService
from app.services.pricing_service import PricingService


class BookingService:
    """Manages the full booking lifecycle."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.inventory = InventoryService(db)
        self.pricing = PricingService()

    async def create_booking(
        self, payload: BookingCreate, current_user: User
    ) -> Booking:
        """Create a new booking with availability check and dynamic pricing.

        Raises:
            NotFoundException: if room not found.
            RoomNotAvailableException: if room is blocked for dates.
        """
        room: Room | None = await self.db.get(Room, payload.room_id)
        if not room:
            raise NotFoundException("Room", str(payload.room_id))

        # Check availability
        available = await self.inventory.is_room_available(
            room.id, payload.check_in_date, payload.check_out_date
        )
        if not available:
            raise RoomNotAvailableException()

        # Calculate price
        total_price = self.pricing.calculate_total(
            room.base_price_per_night,
            payload.check_in_date,
            payload.check_out_date,
        )

        # Create booking
        booking = Booking(
            user_id=current_user.id,
            room_id=room.id,
            check_in_date=payload.check_in_date,
            check_out_date=payload.check_out_date,
            total_price=total_price,
            special_requests=payload.special_requests,
        )
        self.db.add(booking)
        await self.db.flush()

        # Create guest record
        guest_data = payload.guest
        guest = Guest(
            booking_id=booking.id,
            first_name=guest_data.first_name,
            last_name=guest_data.last_name,
            email=guest_data.email,
            phone_number=guest_data.phone_number,
            id_type=guest_data.id_type,
            id_number=guest_data.id_number,
        )
        self.db.add(guest)

        # Block inventory
        await self.inventory.block_dates(
            room.id, payload.check_in_date, payload.check_out_date
        )

        await self.db.flush()
        # Re-fetch to load relationships
        return await self.get_by_id(booking.id, current_user)

    async def get_by_id(self, booking_id: uuid.UUID, current_user: User) -> Booking:
        """Fetch a booking (user can only see their own; admin sees all).

        Raises:
            NotFoundException: if not found.
            ForbiddenException: if user doesn't own the booking and isn't admin.
        """
        booking = await self.db.scalar(
            select(Booking)
            .where(Booking.id == booking_id)
            .options(selectinload(Booking.guest))
        )
        if not booking:
            raise NotFoundException("Booking", str(booking_id))

        if booking.user_id != current_user.id and current_user.role.value != "admin":
            raise ForbiddenException()

        return booking

    async def get_user_bookings(self, current_user: User) -> List[Booking]:
        """Return all bookings for the authenticated user."""
        result = await self.db.execute(
            select(Booking)
            .where(Booking.user_id == current_user.id)
            .options(selectinload(Booking.guest))
            .order_by(Booking.created_at.desc())
        )
        return list(result.scalars().all())

    async def update_status(
        self,
        booking_id: uuid.UUID,
        payload: BookingStatusUpdate,
        current_user: User,
    ) -> Booking:
        """Update booking status (admin or owner)."""
        booking = await self.get_by_id(booking_id, current_user)
        booking.status = payload.status
        await self.db.flush()
        # Re-fetch to ensure relationships are fresh if needed (though get_by_id already does selectinload)
        return await self.get_by_id(booking_id, current_user)

    async def cancel_booking(
        self, booking_id: uuid.UUID, current_user: User
    ) -> Booking:
        """Cancel a booking and release inventory."""
        booking = await self.get_by_id(booking_id, current_user)

        if booking.status == BookingStatus.CANCELLED:
            return booking

        booking.status = BookingStatus.CANCELLED

        # Release inventory
        await self.inventory.release_dates(
            booking.room_id, booking.check_in_date, booking.check_out_date
        )

        await self.db.flush()
        return await self.get_by_id(booking_id, current_user)
