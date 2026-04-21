"""Users API router — /users/profile, /users/{user_id}."""

import uuid

from fastapi import APIRouter

from app.dependencies import DBSession, CurrentUser, AdminUser
from app.schemas.user import UserResponse, UserUpdate, UserRoleUpdate
from app.schemas.responses import APIResponse, MessageResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/profile",
    response_model=APIResponse[UserResponse],
    summary="Get current user profile",
)
async def get_profile(current_user: CurrentUser):
    """Return the authenticated user's profile."""
    return APIResponse(data=UserResponse.model_validate(current_user))


@router.put(
    "/profile",
    response_model=APIResponse[UserResponse],
    summary="Update current user profile",
)
async def update_profile(
    payload: UserUpdate,
    current_user: CurrentUser,
    db: DBSession,
):
    """Partially update the authenticated user's profile fields."""
    service = UserService(db)
    updated = await service.update_profile(current_user, payload)
    return APIResponse(
        message="Profile updated successfully",
        data=UserResponse.model_validate(updated),
    )


@router.get(
    "/{user_id}",
    response_model=APIResponse[UserResponse],
    summary="Get user by ID (Admin only)",
)
async def get_user_by_id(
    user_id: uuid.UUID,
    _: AdminUser,
    db: DBSession,
):
    """Admin-only: fetch any user by their UUID."""
    service = UserService(db)
    user = await service.get_by_id(user_id)
    return APIResponse(data=UserResponse.model_validate(user))


@router.put(
    "/{user_id}/role",
    response_model=APIResponse[UserResponse],
    summary="Update user role (Admin only)",
)
async def update_role(
    user_id: uuid.UUID,
    payload: UserRoleUpdate,
    _: AdminUser,
    db: DBSession,
):
    """Admin-only: change the role of any user."""
    service = UserService(db)
    user = await service.update_role(user_id, payload)
    return APIResponse(
        message="User role updated",
        data=UserResponse.model_validate(user),
    )


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    summary="Deactivate user (Admin only)",
)
async def deactivate_user(
    user_id: uuid.UUID,
    _: AdminUser,
    db: DBSession,
):
    """Admin-only: deactivate a user account."""
    service = UserService(db)
    await service.deactivate(user_id)
    return MessageResponse(message="User deactivated successfully")
