import importlib
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import items as items_service

@pytest.fixture(autouse=True)
def clean_service_state():
    """Vor jedem Test den In-Memory-Store sauber machen."""
    importlib.reload(items_service)
    yield
    # nach dem Test könnte man weitere Aufräumarbeiten machen

@pytest.fixture()
def client() -> TestClient:
    """HTTP-Client für API-Tests."""
    return TestClient(app)
