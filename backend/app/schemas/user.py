"""User Pydantic schemas (DTOs)."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.enums import Gender, Role


# ── Base ──────────────────────────────────────────────────────────────────────
class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=20)
    gender: Optional[Gender] = None


# ── Request Schemas ───────────────────────────────────────────────────────────
class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Schema for updating user profile (all fields optional)."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    profile_picture: Optional[str] = None
    gender: Optional[Gender] = None


class UserRoleUpdate(BaseModel):
    """Schema for admin to update a user's role."""

    role: Role


# ── Response Schemas ──────────────────────────────────────────────────────────
class UserResponse(UserBase):
    """Public user data returned by the API."""

    model_config = {"from_attributes": True}

    id: uuid.UUID
    role: Role
    profile_picture: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class UserInDB(UserResponse):
    """Internal user schema including hashed password."""

    hashed_password: str
