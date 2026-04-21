"""Tests for user management endpoints."""

import pytest
from httpx import AsyncClient
from app.models.user import User


@pytest.mark.asyncio
async def test_get_own_profile(client: AsyncClient, user_auth_headers: dict):
    """Authenticated user can fetch their own profile."""
    response = await client.get("/api/v1/users/profile", headers=user_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_profile_unauthenticated(client: AsyncClient):
    """Unauthenticated request to /profile returns 401."""
    response = await client.get("/api/v1/users/profile")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_profile(client: AsyncClient, user_auth_headers: dict):
    """User can update their own profile fields."""
    response = await client.put(
        "/api/v1/users/profile",
        headers=user_auth_headers,
        json={"first_name": "Updated", "phone_number": "+1234567890"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["first_name"] == "Updated"


@pytest.mark.asyncio
async def test_admin_get_user_by_id(
    client: AsyncClient, admin_auth_headers: dict, test_user: User
):
    """Admin can fetch any user by ID."""
    response = await client.get(
        f"/api/v1/users/{test_user.id}", headers=admin_auth_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_regular_user_cannot_get_user_by_id(
    client: AsyncClient, user_auth_headers: dict, test_user: User
):
    """Regular user cannot access the admin-only user-by-ID endpoint."""
    response = await client.get(
        f"/api/v1/users/{test_user.id}", headers=user_auth_headers
    )
    assert response.status_code == 403
