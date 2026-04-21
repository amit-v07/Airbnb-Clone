"""Authentication service — register, login, token refresh."""

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, UnauthorizedException
from app.models.user import User
from app.models.enums import Role
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest, TokenResponse
from app.security.password import hash_password, verify_password
from app.security.jwt_handler import create_access_token, create_refresh_token, verify_token


class AuthService:
    """Handles user registration, login, and token refresh."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def register(self, payload: UserCreate) -> User:
        """Register a new user.

        Raises:
            ConflictException: if email is already in use.
        """
        # Check for duplicate email
        existing = await self.db.scalar(
            select(User).where(User.email == payload.email)
        )
        if existing:
            raise ConflictException("A user with this email address already exists")

        user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            hashed_password=hash_password(payload.password),
            phone_number=payload.phone_number,
            gender=payload.gender,
            role=Role.USER,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def login(self, payload: LoginRequest) -> TokenResponse:
        """Validate credentials and return a token pair.

        Raises:
            UnauthorizedException: if email not found or password wrong.
        """
        user: Optional[User] = await self.db.scalar(
            select(User).where(User.email == payload.email)
        )
        if not user or not verify_password(payload.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedException("Account is deactivated")

        return TokenResponse(
            access_token=create_access_token(str(user.id), user.role.value),
            refresh_token=create_refresh_token(str(user.id), user.role.value),
        )

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Issue a new access token using a valid refresh token.

        Raises:
            UnauthorizedException: if refresh token is invalid or user not found.
        """
        try:
            payload = verify_token(refresh_token, expected_type="refresh")
        except ValueError as exc:
            raise UnauthorizedException(str(exc)) from exc

        user_id = payload.get("sub")
        user: Optional[User] = await self.db.get(User, uuid.UUID(user_id))
        if not user or not user.is_active:
            raise UnauthorizedException("User not found or deactivated")

        return TokenResponse(
            access_token=create_access_token(str(user.id), user.role.value),
            refresh_token=create_refresh_token(str(user.id), user.role.value),
        )
