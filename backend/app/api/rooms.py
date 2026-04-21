"""Rooms API router — /hotels/{hotel_id}/rooms, /rooms/{room_id}."""

import uuid
from typing import List

from fastapi import APIRouter

from app.dependencies import DBSession, AdminUser, HostOrAdminUser, CurrentUser
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse
from app.schemas.responses import APIResponse, MessageResponse
from app.services.room_service import RoomService

router = APIRouter(tags=["Rooms"])


@router.get(
    "/hotels/{hotel_id}/rooms",
    response_model=APIResponse[List[RoomResponse]],
    summary="List rooms in a hotel",
)
async def list_rooms(hotel_id: uuid.UUID, db: DBSession):
    """Return all rooms for a given hotel. Public endpoint."""
    service = RoomService(db)
    rooms = await service.get_by_hotel(hotel_id)
    return APIResponse(data=[RoomResponse.model_validate(r) for r in rooms])


@router.post(
    "/hotels/{hotel_id}/rooms",
    response_model=APIResponse[RoomResponse],
    status_code=201,
    summary="Add a room to a hotel (Admin/Host only)",
)
async def create_room(
    hotel_id: uuid.UUID,
    payload: RoomCreate,
    _: HostOrAdminUser,
    db: DBSession,
):
    """Add a new room under a specific hotel (Admin or Host)."""
    service = RoomService(db)
    room = await service.create(hotel_id, payload)
    return APIResponse(
        message="Room created successfully",
        data=RoomResponse.model_validate(room),
    )


@router.put(
    "/rooms/{room_id}",
    response_model=APIResponse[RoomResponse],
    summary="Update room details (Admin/Host only)",
)
async def update_room(
    room_id: uuid.UUID,
    payload: RoomUpdate,
    _: HostOrAdminUser,
    db: DBSession,
):
    """Partially update a room's details."""
    service = RoomService(db)
    room = await service.update(room_id, payload)
    return APIResponse(
        message="Room updated successfully",
        data=RoomResponse.model_validate(room),
    )


@router.delete(
    "/rooms/{room_id}",
    response_model=MessageResponse,
    summary="Delete a room (Admin only)",
)
async def delete_room(
    room_id: uuid.UUID,
    _: AdminUser,
    db: DBSession,
):
    """Admin-only: permanently delete a room."""
    service = RoomService(db)
    await service.delete(room_id)
    return MessageResponse(message="Room deleted successfully")
