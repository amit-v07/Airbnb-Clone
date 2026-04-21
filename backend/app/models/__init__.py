"""Models package — import all ORM models here so Alembic can detect them."""

from app.models.user import User
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.booking import Booking
from app.models.guest import Guest
from app.models.inventory import RoomInventory
from app.models.enums import (
    Role,
    Gender,
    BookingStatus,
    RoomType,
    PaymentStatus,
)

__all__ = [
    "User",
    "Hotel",
    "Room",
    "Booking",
    "Guest",
    "RoomInventory",
    "Role",
    "Gender",
    "BookingStatus",
    "RoomType",
    "PaymentStatus",
]
