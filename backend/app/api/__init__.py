"""API package — collect all routers."""

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.hotels import router as hotels_router
from app.api.rooms import router as rooms_router
from app.api.bookings import router as bookings_router
from app.api.payments import router as payments_router
from app.api.inventory import router as inventory_router

__all__ = [
    "auth_router",
    "users_router",
    "hotels_router",
    "rooms_router",
    "bookings_router",
    "payments_router",
    "inventory_router",
]
