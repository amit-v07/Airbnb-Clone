"""
FastAPI application entry point.

Run with:
    uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.exceptions.handlers import register_exception_handlers
from app.api import (
    auth_router,
    users_router,
    hotels_router,
    rooms_router,
    bookings_router,
    payments_router,
    inventory_router,
)


# ── Lifespan ──────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application startup/shutdown lifecycle handler."""
    # Startup
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} is starting up...")
    yield
    # Shutdown
    print("🛑 Application shutting down...")


# ── App Factory ───────────────────────────────────────────────────────────────
def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
## Airbnb Clone API

A modern, high-performance booking system built with **FastAPI** and **PostgreSQL**.

### Features
- 🔐 JWT-based authentication with refresh tokens
- 👥 Role-based access control (Admin / Host / User)
- 🏨 Hotel & Room management with dynamic search
- 📅 Booking system with inventory management
- 💳 Stripe payment integration
- 💰 Dynamic pricing strategies (Holiday, Surge, Occupancy, Urgency)
        """,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Exception Handlers ────────────────────────────────────────────────────
    register_exception_handlers(app)

    # ── Routers ───────────────────────────────────────────────────────────────
    API_PREFIX = "/api/v1"

    app.include_router(auth_router, prefix=API_PREFIX)
    app.include_router(users_router, prefix=API_PREFIX)
    app.include_router(hotels_router, prefix=API_PREFIX)
    app.include_router(rooms_router, prefix=API_PREFIX)
    app.include_router(bookings_router, prefix=API_PREFIX)
    app.include_router(payments_router, prefix=API_PREFIX)
    app.include_router(inventory_router, prefix=API_PREFIX)

    # ── Health Check ──────────────────────────────────────────────────────────
    @app.get("/health", tags=["Health"], summary="Health check")
    async def health_check():
        """Simple health check endpoint."""
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }

    return app


# ── Application Instance ──────────────────────────────────────────────────────
app = create_app()
