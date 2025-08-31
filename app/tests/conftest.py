# app/tests/conftest.py
import os
import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from sqlalchemy.pool import NullPool  # <<< wichtig
# ganz unten in conftest.py


from app.main import app
from app.db.session import get_session


@pytest.fixture
def anyio_backend():
    return "asyncio"


TEST_DATABASE_URL = (
    os.environ.get("TEST_DATABASE_URL")
    or "postgresql+asyncpg://app:postgres@localhost:5432/app_testdb"
)

# Engine ohne Pool (vermeidet Cross-Thread-Ärger im TestClient)
test_engine = create_async_engine(TEST_DATABASE_URL, future=True, poolclass=NullPool)

TestSessionLocal = async_sessionmaker(
    bind=test_engine, expire_on_commit=False, autoflush=False, class_=AsyncSession
)

async def _truncate_items():
    async with test_engine.begin() as conn:
        # Items-Tabelle leeren + IDs zurücksetzen (erweitere bei neuen Tabellen)
        await conn.execute(text("TRUNCATE TABLE items RESTART IDENTITY CASCADE;"))

def _run_async(coro):
    """Hilfsfunktion: läuft auch, wenn bereits ein Event Loop aktiv ist."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        # in Sync-Tests ist meist kein Loop aktiv; falls doch: separater Task
        return loop.create_task(coro)

@pytest.fixture(autouse=True)
def _clean_db():
    _run_async(_truncate_items())
    yield

@pytest.fixture(autouse=True)
def override_get_session():
    async def _get_session_override():
        async with TestSessionLocal() as session:
            yield session
    app.dependency_overrides[get_session] = _get_session_override
    yield
    app.dependency_overrides.clear()

@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture()
async def db_session():
    async with TestSessionLocal() as session:
        yield session
