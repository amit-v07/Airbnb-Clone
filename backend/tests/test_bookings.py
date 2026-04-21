"""Tests for booking endpoints."""

import pytest
from datetime import date, timedelta
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_list_booking(
    client: AsyncClient, admin_auth_headers: dict, user_auth_headers: dict
):
    """User can create a booking and list it."""
    # Create hotel
    hotel_resp = await client.post(
        "/api/v1/hotels",
        json={
            "name": "Booking Test Hotel",
            "address": "1 Test St",
            "city": "TestCity",
            "country": "USA",
        },
        headers=admin_auth_headers,
    )
    hotel_id = hotel_resp.json()["data"]["id"]

    # Create room
    room_resp = await client.post(
        f"/api/v1/hotels/{hotel_id}/rooms",
        json={
            "room_number": "101",
            "room_type": "single",
            "capacity": 1,
            "base_price_per_night": "100.00",
        },
        headers=admin_auth_headers,
    )
    room_id = room_resp.json()["data"]["id"]

    # Create booking
    check_in = (date.today() + timedelta(days=5)).isoformat()
    check_out = (date.today() + timedelta(days=8)).isoformat()
    booking_payload = {
        "room_id": room_id,
        "check_in_date": check_in,
        "check_out_date": check_out,
        "guest": {
            "first_name": "John",
            "last_name": "Traveler",
            "email": "john@travel.com",
        },
    }
    booking_resp = await client.post(
        "/api/v1/bookings", json=booking_payload, headers=user_auth_headers
    )
    assert booking_resp.status_code == 201
    booking_id = booking_resp.json()["data"]["id"]
    assert booking_resp.json()["data"]["status"] == "pending"

    # List bookings
    list_resp = await client.get("/api/v1/bookings", headers=user_auth_headers)
    assert list_resp.status_code == 200
    ids = [b["id"] for b in list_resp.json()["data"]]
    assert booking_id in ids


@pytest.mark.asyncio
async def test_cancel_booking(
    client: AsyncClient, admin_auth_headers: dict, user_auth_headers: dict
):
    """User can cancel their own booking."""
    hotel_resp = await client.post(
        "/api/v1/hotels",
        json={
            "name": "Cancel Hotel",
            "address": "2 Test St",
            "city": "CancelCity",
            "country": "USA",
        },
        headers=admin_auth_headers,
    )
    hotel_id = hotel_resp.json()["data"]["id"]

    room_resp = await client.post(
        f"/api/v1/hotels/{hotel_id}/rooms",
        json={
            "room_number": "202",
            "room_type": "double",
            "capacity": 2,
            "base_price_per_night": "150.00",
        },
        headers=admin_auth_headers,
    )
    room_id = room_resp.json()["data"]["id"]

    check_in = (date.today() + timedelta(days=10)).isoformat()
    check_out = (date.today() + timedelta(days=12)).isoformat()
    booking_resp = await client.post(
        "/api/v1/bookings",
        json={
            "room_id": room_id,
            "check_in_date": check_in,
            "check_out_date": check_out,
            "guest": {
                "first_name": "Cancel",
                "last_name": "Guest",
                "email": "cancel@guest.com",
            },
        },
        headers=user_auth_headers,
    )
    booking_id = booking_resp.json()["data"]["id"]

    cancel_resp = await client.delete(
        f"/api/v1/bookings/{booking_id}", headers=user_auth_headers
    )
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["message"] == "Booking cancelled successfully"
