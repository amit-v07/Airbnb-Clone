"""Room service — CRUD within a hotel context."""

import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundException
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate


class RoomService:
    """Business logic for room management."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, hotel_id: uuid.UUID, payload: RoomCreate) -> Room:
        """Add a new room to a hotel."""
        room = Room(hotel_id=hotel_id, **payload.model_dump())
        self.db.add(room)
        await self.db.flush()
        await self.db.refresh(room)
        return room

    async def get_by_id(self, room_id: uuid.UUID) -> Room:
        """Fetch a room by UUID.

        Raises:
            NotFoundException: if room not found.
        """
        room = await self.db.get(Room, room_id)
        if not room:
            raise NotFoundException("Room", str(room_id))
        return room

    async def get_by_hotel(self, hotel_id: uuid.UUID) -> List[Room]:
        """List all rooms for a specific hotel."""
        result = await self.db.execute(
            select(Room)
            .where(Room.hotel_id == hotel_id)
            .order_by(Room.room_number)
        )
        return list(result.scalars().all())

    async def update(self, room_id: uuid.UUID, payload: RoomUpdate) -> Room:
        """Partially update a room."""
        room = await self.get_by_id(room_id)
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(room, field, value)
        await self.db.flush()
        await self.db.refresh(room)
        return room

    async def delete(self, room_id: uuid.UUID) -> None:
        """Delete a room."""
        room = await self.get_by_id(room_id)
        await self.db.delete(room)
        await self.db.flush()
