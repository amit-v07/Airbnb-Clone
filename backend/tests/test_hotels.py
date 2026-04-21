"""Tests for hotel management endpoints."""

import pytest
from httpx import AsyncClient


HOTEL_PAYLOAD = {
    "name": "Grand Azure Hotel",
    "address": "123 Ocean Drive",
    "city": "Miami",
    "country": "USA",
    "star_rating": 5,
    "description": "Luxury beachfront hotel",
}


@pytest.mark.asyncio
async def test_list_hotels_public(client: AsyncClient):
    """Hotel listing is publicly accessible without authentication."""
    response = await client.get("/api/v1/hotels")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_create_hotel_admin(client: AsyncClient, admin_auth_headers: dict):
    """Admin can create a hotel."""
    response = await client.post(
        "/api/v1/hotels", json=HOTEL_PAYLOAD, headers=admin_auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["name"] == "Grand Azure Hotel"
    assert data["data"]["city"] == "Miami"


@pytest.mark.asyncio
async def test_create_hotel_user_forbidden(
    client: AsyncClient, user_auth_headers: dict
):
    """Regular user cannot create hotels (403)."""
    response = await client.post(
        "/api/v1/hotels", json=HOTEL_PAYLOAD, headers=user_auth_headers
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_hotel_by_id(client: AsyncClient, admin_auth_headers: dict):
    """Can fetch a hotel by ID after creating it."""
    create_resp = await client.post(
        "/api/v1/hotels", json=HOTEL_PAYLOAD, headers=admin_auth_headers
    )
    hotel_id = create_resp.json()["data"]["id"]

    response = await client.get(f"/api/v1/hotels/{hotel_id}")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == hotel_id


@pytest.mark.asyncio
async def test_get_hotel_not_found(client: AsyncClient):
    """Non-existent hotel returns 404."""
    response = await client.get(
        "/api/v1/hotels/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_search_hotels_by_city(client: AsyncClient, admin_auth_headers: dict):
    """Hotels can be filtered by city."""
    await client.post(
        "/api/v1/hotels", json=HOTEL_PAYLOAD, headers=admin_auth_headers
    )
    response = await client.get("/api/v1/hotels?city=Miami")
    assert response.status_code == 200
    items = response.json()["items"]
    assert all("Miami" in h["city"] for h in items)
