"""Application-wide enumerations."""

import enum


class Role(str, enum.Enum):
    """User roles for role-based access control."""
    ADMIN = "admin"
    HOST = "host"
    USER = "user"


class Gender(str, enum.Enum):
    """User gender options."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class BookingStatus(str, enum.Enum):
    """Lifecycle states of a booking."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"


class RoomType(str, enum.Enum):
    """Types of rooms available in a hotel."""
    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"
    DELUXE = "deluxe"
    PENTHOUSE = "penthouse"
    STUDIO = "studio"


class PaymentStatus(str, enum.Enum):
    """Payment states for a booking."""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"
