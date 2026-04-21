"""Schemas package."""

from app.schemas.responses import APIResponse, PaginatedResponse, MessageResponse, ErrorResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserRoleUpdate
from app.schemas.hotel import HotelCreate, HotelUpdate, HotelResponse, HotelSearchFilter
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse, RoomWithPriceResponse
from app.schemas.booking import BookingCreate, BookingStatusUpdate, BookingResponse, GuestInfo, GuestResponse
from app.schemas.payment import CheckoutRequest, CheckoutResponse, PaymentStatusResponse
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest

__all__ = [
    "APIResponse", "PaginatedResponse", "MessageResponse", "ErrorResponse",
    "UserCreate", "UserUpdate", "UserResponse", "UserRoleUpdate",
    "HotelCreate", "HotelUpdate", "HotelResponse", "HotelSearchFilter",
    "RoomCreate", "RoomUpdate", "RoomResponse", "RoomWithPriceResponse",
    "BookingCreate", "BookingStatusUpdate", "BookingResponse", "GuestInfo", "GuestResponse",
    "CheckoutRequest", "CheckoutResponse", "PaymentStatusResponse",
    "LoginRequest", "TokenResponse", "RefreshRequest",
]
