"""User service — profile management and admin operations."""

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundException, ForbiddenException
from app.models.user import User
from app.schemas.user import UserUpdate, UserRoleUpdate


class UserService:
    """Manages user profile read/update operations."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, user_id: uuid.UUID) -> User:
        """Fetch a user by UUID.

        Raises:
            NotFoundException: if user does not exist.
        """
        user = await self.db.get(User, user_id)
        if not user:
            raise NotFoundException("User", str(user_id))
        return user

    async def get_profile(self, current_user: User) -> User:
        """Return the current authenticated user's profile."""
        return current_user

    async def update_profile(
        self, current_user: User, payload: UserUpdate
    ) -> User:
        """Apply partial updates to the user's own profile."""
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(current_user, field, value)
        await self.db.flush()
        await self.db.refresh(current_user)
        return current_user

    async def update_role(
        self, target_user_id: uuid.UUID, payload: UserRoleUpdate
    ) -> User:
        """Admin-only: change the role of another user."""
        user = await self.get_by_id(target_user_id)
        user.role = payload.role
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def deactivate(self, target_user_id: uuid.UUID) -> User:
        """Admin-only: deactivate a user account."""
        user = await self.get_by_id(target_user_id)
        user.is_active = False
        await self.db.flush()
        return user
