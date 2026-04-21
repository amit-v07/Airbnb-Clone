"""Hotels API router — /hotels."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query

from app.dependencies import DBSession, AdminUser, CurrentUser
from app.schemas.hotel import HotelCreate, HotelUpdate, HotelResponse, HotelSearchFilter
from app.schemas.responses import APIResponse, PaginatedResponse, MessageResponse
from app.services.hotel_service import HotelService

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="Browse and search hotels",
)
async def list_hotels(
    db: DBSession,
    city: Optional[str] = Query(None, description="Filter by city"),
    country: Optional[str] = Query(None, description="Filter by country"),
    min_rating: Optional[int] = Query(None, ge=1, le=5),
    max_rating: Optional[int] = Query(None, ge=1, le=5),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """Browse hotels with optional filters. Public endpoint."""
    filters = HotelSearchFilter(
        city=city,
        country=country,
        min_rating=min_rating,
        max_rating=max_rating,
        page=page,
        page_size=page_size,
    )
    service = HotelService(db)
    result = await service.search(filters)
    result.items = [HotelResponse.model_validate(h) for h in result.items]
    return result


@router.get(
    "/{hotel_id}",
    response_model=APIResponse[HotelResponse],
    summary="Get hotel details",
)
async def get_hotel(hotel_id: uuid.UUID, db: DBSession):
    """Return details for a specific hotel. Public endpoint."""
    service = HotelService(db)
    hotel = await service.get_by_id(hotel_id)
    return APIResponse(data=HotelResponse.model_validate(hotel))


@router.post(
    "",
    response_model=APIResponse[HotelResponse],
    status_code=201,
    summary="Create a new hotel (Admin only)",
)
async def create_hotel(
    payload: HotelCreate,
    _: AdminUser,
    db: DBSession,
):
    """Admin-only: add a new hotel to the platform."""
    service = HotelService(db)
    hotel = await service.create(payload)
    return APIResponse(
        message="Hotel created successfully",
        data=HotelResponse.model_validate(hotel),
    )


@router.put(
    "/{hotel_id}",
    response_model=APIResponse[HotelResponse],
    summary="Update hotel details (Admin only)",
)
async def update_hotel(
    hotel_id: uuid.UUID,
    payload: HotelUpdate,
    _: AdminUser,
    db: DBSession,
):
    """Admin-only: update an existing hotel."""
    service = HotelService(db)
    hotel = await service.update(hotel_id, payload)
    return APIResponse(
        message="Hotel updated successfully",
        data=HotelResponse.model_validate(hotel),
    )


@router.delete(
    "/{hotel_id}",
    response_model=MessageResponse,
    summary="Delete a hotel (Admin only)",
)
async def delete_hotel(
    hotel_id: uuid.UUID,
    _: AdminUser,
    db: DBSession,
):
    """Admin-only: permanently delete a hotel and all its rooms."""
    service = HotelService(db)
    await service.delete(hotel_id)
    return MessageResponse(message="Hotel deleted successfully")
