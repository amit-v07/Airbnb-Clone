"""Inventory service — manages room availability per date."""

import uuid
from datetime import date, timedelta
from typing import List

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory import RoomInventory


class InventoryService:
    """Manages room day-by-day availability (inventory blocks)."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def is_room_available(
        self, room_id: uuid.UUID, check_in: date, check_out: date
    ) -> bool:
        """Return True if the room has no conflicting inventory blocks."""
        result = await self.db.execute(
            select(RoomInventory).where(
                and_(
                    RoomInventory.room_id == room_id,
                    RoomInventory.date >= check_in,
                    RoomInventory.date < check_out,
                    RoomInventory.is_available == False,  # noqa: E712
                )
            )
        )
        return result.scalars().first() is None

    async def block_dates(
        self, room_id: uuid.UUID, check_in: date, check_out: date
    ) -> None:
        """Mark each date in the range as unavailable (booked)."""
        current = check_in
        while current < check_out:
            existing = await self.db.scalar(
                select(RoomInventory).where(
                    and_(
                        RoomInventory.room_id == room_id,
                        RoomInventory.date == current,
                    )
                )
            )
            if existing:
                existing.is_available = False
                existing.reserved_count += 1
            else:
                self.db.add(
                    RoomInventory(
                        room_id=room_id,
                        date=current,
                        is_available=False,
                        reserved_count=1,
                    )
                )
            current += timedelta(days=1)
        await self.db.flush()

    async def release_dates(
        self, room_id: uuid.UUID, check_in: date, check_out: date
    ) -> None:
        """Release inventory (set available=True) for a cancelled booking."""
        current = check_in
        while current < check_out:
            existing = await self.db.scalar(
                select(RoomInventory).where(
                    and_(
                        RoomInventory.room_id == room_id,
                        RoomInventory.date == current,
                    )
                )
            )
            if existing and existing.reserved_count > 0:
                existing.reserved_count -= 1
                if existing.reserved_count == 0:
                    existing.is_available = True
            current += timedelta(days=1)
        await self.db.flush()

    async def get_availability(
        self, room_id: uuid.UUID, start: date, end: date
    ) -> List[RoomInventory]:
        """Fetch inventory records for a room within a date range."""
        result = await self.db.execute(
            select(RoomInventory).where(
                and_(
                    RoomInventory.room_id == room_id,
                    RoomInventory.date >= start,
                    RoomInventory.date < end,
                )
            ).order_by(RoomInventory.date)
        )
        return list(result.scalars().all())
