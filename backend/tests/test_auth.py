"""Tests for authentication endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_signup_success(client: AsyncClient):
    """A new user can register successfully."""
    response = await client.post(
        "/api/v1/auth/signup",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password": "SecurePass1",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "jane@example.com"
    assert "hashed_password" not in data["data"]


@pytest.mark.asyncio
async def test_signup_duplicate_email(client: AsyncClient):
    """Registering with an existing email returns 409."""
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "duplicate@example.com",
        "password": "SecurePass1",
    }
    await client.post("/api/v1/auth/signup", json=payload)
    response = await client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Valid credentials return access and refresh tokens."""
    await client.post(
        "/api/v1/auth/signup",
        json={
            "first_name": "Login",
            "last_name": "Test",
            "email": "logintest@example.com",
            "password": "LoginPass1",
        },
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "logintest@example.com", "password": "LoginPass1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Wrong password returns 401."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "WrongPassword1"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_weak_password_signup(client: AsyncClient):
    """Signing up with a weak password returns 422."""
    response = await client.post(
        "/api/v1/auth/signup",
        json={
            "first_name": "Weak",
            "last_name": "Pass",
            "email": "weak@example.com",
            "password": "short",
        },
    )
    assert response.status_code == 422
