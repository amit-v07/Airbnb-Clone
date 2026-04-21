"""Inventory API router — /inventory."""

import uuid
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Query

from app.dependencies import DBSession, AdminUser, HostOrAdminUser
from app.schemas.responses import APIResponse
from app.services.inventory_service import InventoryService
from pydantic import BaseModel


class AvailabilityResponse(BaseModel):
    room_id: uuid.UUID
    date: date
    is_available: bool
    reserved_count: int

    model_config = {"from_attributes": True}


router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get(
    "",
    response_model=APIResponse[List[AvailabilityResponse]],
    summary="Get room inventory/availability for a date range",
)
async def get_room_inventory(
    room_id: uuid.UUID,
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: DBSession = ...,
    _: HostOrAdminUser = ...,
):
    """Return availability records for a room within a date range (Admin/Host)."""
    service = InventoryService(db)
    records = await service.get_availability(room_id, start_date, end_date)
    return APIResponse(
        data=[AvailabilityResponse.model_validate(r) for r in records]
    )
