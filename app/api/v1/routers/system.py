# app/api/v1/routers/system.py
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/time", tags=["system"], summary="Get current server time (UTC)")
def get_time() -> dict[str, str]:
    return {"server_time": datetime.now(UTC).isoformat()}


@router.get("/health", tags=["system"], summary="Health check (liveness/readiness)")
def get_health() -> dict[str, Any]:
    return {
        "status": "ok",
        "time": datetime.now(UTC).isoformat(),
        "services": {"api": "ok"},
    }


@router.get("/version", tags=["system"], summary="Get application version info")
def get_version() -> dict[str, Any]:
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "commit": settings.GIT_COMMIT,
        "build_time": settings.BUILD_TIME,
    }
