"""Pytest configuration — fixtures for test DB, client, and auth."""

import asyncio
import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.db.base import Base
from app.db.database import get_db
from app.models.user import User
from app.models.enums import Role
from app.security.password import hash_password
from app.security.jwt_handler import create_access_token

# ── Test Database ─────────────────────────────────────────────────────────────
# In Docker, 'db' is the hostname. Local fallback is localhost.
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", 
    "postgresql+asyncpg://airbnb_user:airbnb_password@db:5432/airbnb_test_db"
)

test_engine = create_async_engine(
    TEST_DATABASE_URL, 
    echo=False,
    poolclass=NullPool
)
TestSessionLocal = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Use a single event loop for the entire test session."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """Create all tables at the start of the test session, drop at end."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a rolled-back DB session per test (no data leaks)."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Async test client with DB override."""
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# ── Test User Fixtures ────────────────────────────────────────────────────────
@pytest_asyncio.fixture
async def test_user(db: AsyncSession) -> User:
    """Create a regular test user."""
    user = User(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        hashed_password=hash_password("TestPass123"),
        role=Role.USER,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture
async def admin_user(db: AsyncSession) -> User:
    """Create an admin test user."""
    user = User(
        first_name="Admin",
        last_name="User",
        email="admin@example.com",
        hashed_password=hash_password("AdminPass123"),
        role=Role.ADMIN,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@pytest.fixture
def user_auth_headers(test_user: User) -> dict:
    """HTTP headers with a valid user access token."""
    token = create_access_token(str(test_user.id), test_user.role.value)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_auth_headers(admin_user: User) -> dict:
    """HTTP headers with a valid admin access token."""
    token = create_access_token(str(admin_user.id), admin_user.role.value)
    return {"Authorization": f"Bearer {token}"}
