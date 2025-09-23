# app/tests/conftest.py
import asyncio
import os
from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.db.session import get_session
from app.main import app

# ---- Test-DB URL ----
TEST_DATABASE_URL = (
    os.environ.get("TEST_DATABASE_URL")
    or "postgresql+asyncpg://app:postgres@localhost:5432/app_testdb"
)

# ---- Async Engine ohne Pool (stabil mit TestClient) ----
test_engine = create_async_engine(TEST_DATABASE_URL, future=True, poolclass=NullPool)

# ---- Sessionmaker für Tests ----
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)


# ---- Datenbank vor jedem Test leeren ----
async def _truncate_all() -> None:
    async with test_engine.begin() as conn:
        # Reihenfolge ist egal dank CASCADE; ergänze weitere Tabellen hier
        await conn.execute(text("TRUNCATE TABLE items RESTART IDENTITY CASCADE;"))
        await conn.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
        await conn.execute(text("TRUNCATE TABLE bikes RESTART IDENTITY CASCADE;"))
        await conn.execute(text("TRUNCATE TABLE maintenances RESTART IDENTITY CASCADE;"))


@pytest.fixture(autouse=True)
def _clean_db() -> Generator[None, None, None]:
    asyncio.run(_truncate_all())
    yield


# ---- FastAPI Dependency Override: App-Endpoints nutzen Test-Session ----
@pytest.fixture(autouse=True)
def override_get_session() -> Generator[None, None, None]:
    async def _get_session_override() -> AsyncGenerator[AsyncSession, None]:
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = _get_session_override
    yield
    app.dependency_overrides.clear()


# ---- HTTP-Client für API-Tests ----
@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


# ---- Direkt-Session für Service-Unit-Tests ----
@pytest.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session


# ---- AnyIO-Backend fest auf asyncio pinnen (verhindert Trio-Parametrisierung) ----
@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
