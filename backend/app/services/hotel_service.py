"""Hotel service — CRUD and search/filter logic."""

import uuid
from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundException
from app.models.hotel import Hotel
from app.schemas.hotel import HotelCreate, HotelUpdate, HotelSearchFilter
from app.schemas.responses import PaginatedResponse


class HotelService:
    """Business logic for hotel management and browsing."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, payload: HotelCreate) -> Hotel:
        """Create a new hotel listing."""
        hotel = Hotel(**payload.model_dump())
        self.db.add(hotel)
        await self.db.flush()
        await self.db.refresh(hotel)
        return hotel

    async def get_by_id(self, hotel_id: uuid.UUID) -> Hotel:
        """Fetch a hotel by UUID.

        Raises:
            NotFoundException: if hotel does not exist.
        """
        hotel = await self.db.get(Hotel, hotel_id)
        if not hotel:
            raise NotFoundException("Hotel", str(hotel_id))
        return hotel

    async def search(self, filters: HotelSearchFilter) -> PaginatedResponse:
        """Browse hotels with optional city/country/rating filters."""
        query = select(Hotel)

        if filters.city:
            query = query.where(Hotel.city.ilike(f"%{filters.city}%"))
        if filters.country:
            query = query.where(Hotel.country.ilike(f"%{filters.country}%"))
        if filters.min_rating is not None:
            query = query.where(Hotel.star_rating >= filters.min_rating)
        if filters.max_rating is not None:
            query = query.where(Hotel.star_rating <= filters.max_rating)

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query) or 0

        # Paginate
        offset = (filters.page - 1) * filters.page_size
        result = await self.db.execute(
            query.offset(offset).limit(filters.page_size).order_by(Hotel.created_at.desc())
        )
        hotels = list(result.scalars().all())
        total_pages = (total + filters.page_size - 1) // filters.page_size

        return PaginatedResponse(
            items=hotels,
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            total_pages=total_pages,
        )

    async def update(self, hotel_id: uuid.UUID, payload: HotelUpdate) -> Hotel:
        """Partially update a hotel."""
        hotel = await self.get_by_id(hotel_id)
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(hotel, field, value)
        await self.db.flush()
        await self.db.refresh(hotel)
        return hotel

    async def delete(self, hotel_id: uuid.UUID) -> None:
        """Delete a hotel (cascades to rooms and inventory)."""
        hotel = await self.get_by_id(hotel_id)
        await self.db.delete(hotel)
        await self.db.flush()
