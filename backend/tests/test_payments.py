"""Tests for payment endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_checkout_requires_auth(client: AsyncClient):
    """Payment checkout requires authentication."""
    response = await client.post(
        "/api/v1/payments/checkout",
        json={
            "booking_id": "00000000-0000-0000-0000-000000000000",
            "success_url": "http://localhost:3000/success",
            "cancel_url": "http://localhost:3000/cancel",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_checkout_invalid_booking(
    client: AsyncClient, user_auth_headers: dict
):
    """Checkout with non-existent booking ID returns 404."""
    response = await client.post(
        "/api/v1/payments/checkout",
        json={
            "booking_id": "00000000-0000-0000-0000-000000000000",
            "success_url": "http://localhost:3000/success",
            "cancel_url": "http://localhost:3000/cancel",
        },
        headers=user_auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_payment_status_requires_auth(client: AsyncClient):
    """Payment status endpoint requires authentication."""
    response = await client.get(
        "/api/v1/bookings/00000000-0000-0000-0000-000000000000/payment-status"
    )
    assert response.status_code == 401
