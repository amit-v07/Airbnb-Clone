"""FastAPI dependency injection — DB session and current user extraction."""

import uuid
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.exceptions import UnauthorizedException, ForbiddenException
from app.models.user import User
from app.models.enums import Role
from app.security.jwt_handler import verify_token

# ── Auth Scheme ───────────────────────────────────────────────────────────────
bearer_scheme = HTTPBearer(auto_error=False)

# ── Type Aliases ──────────────────────────────────────────────────────────────
DBSession = Annotated[AsyncSession, Depends(get_db)]
BearerToken = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]


async def get_current_user(
    credentials: BearerToken,
    db: DBSession,
) -> User:
    """Extract and validate the JWT bearer token, return the authenticated user.

    Raises:
        UnauthorizedException: if token is missing, invalid, or user not found.
    """
    if not credentials:
        raise UnauthorizedException("No authentication token provided")

    try:
        payload = verify_token(credentials.credentials, expected_type="access")
    except ValueError as exc:
        raise UnauthorizedException(str(exc)) from exc

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException("Token subject missing")

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise UnauthorizedException("Invalid token subject")

    user: User | None = await db.get(User, user_id)
    if not user or not user.is_active:
        raise UnauthorizedException("User not found or deactivated")

    return user


async def get_admin_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Require the current user to have ADMIN role.

    Raises:
        ForbiddenException: if user is not an admin.
    """
    if current_user.role != Role.ADMIN:
        raise ForbiddenException("Administrator privileges required")
    return current_user


async def get_host_or_admin_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Require the current user to be HOST or ADMIN."""
    if current_user.role not in (Role.ADMIN, Role.HOST):
        raise ForbiddenException("Host or Administrator privileges required")
    return current_user


# ── Convenience Type Aliases for Route Signatures ─────────────────────────────
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(get_admin_user)]
HostOrAdminUser = Annotated[User, Depends(get_host_or_admin_user)]
