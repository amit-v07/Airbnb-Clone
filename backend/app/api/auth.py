"""Authentication API router — /auth/signup, /auth/login, /auth/refresh."""

from fastapi import APIRouter

from app.dependencies import DBSession
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.schemas.responses import APIResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=APIResponse[UserResponse],
    status_code=201,
    summary="Register a new user account",
)
async def signup(payload: UserCreate, db: DBSession):
    """Register a new user. Raises 409 if email already exists."""
    service = AuthService(db)
    user = await service.register(payload)
    return APIResponse(
        message="Account created successfully",
        data=UserResponse.model_validate(user),
    )


@router.post(
    "/login",
    response_model=APIResponse[TokenResponse],
    summary="Login and receive JWT tokens",
)
async def login(payload: LoginRequest, db: DBSession):
    """Authenticate with email/password and receive an access + refresh token pair."""
    service = AuthService(db)
    tokens = await service.login(payload)
    return APIResponse(message="Login successful", data=tokens)


@router.post(
    "/refresh",
    response_model=APIResponse[TokenResponse],
    summary="Refresh access token using a refresh token",
)
async def refresh(payload: RefreshRequest, db: DBSession):
    """Exchange a valid refresh token for a new token pair."""
    service = AuthService(db)
    tokens = await service.refresh_token(payload.refresh_token)
    return APIResponse(message="Token refreshed", data=tokens)
