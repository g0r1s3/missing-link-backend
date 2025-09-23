# app/api/v1/routers/maintenances.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.maintenance import MaintenanceCreate, MaintenanceRead, MaintenanceUpdate
from app.services import maintenances as service

router = APIRouter(prefix="/maintenances", tags=["maintenances"])


@router.get(
    "",
    response_model=list[MaintenanceRead],
    summary="List maintenances (optionally for a specific bike)",
)
async def list_maintenances(
    bike_id: int | None = Query(default=None, description="Filter by bike_id"),
    session: AsyncSession = Depends(get_session),
    current: User = Depends(get_current_user),
) -> list[MaintenanceRead]:
    items = await service.list_for_user(session, owner_id=current.id, bike_id=bike_id)
    return [MaintenanceRead.model_validate(x.__dict__) for x in items]


@router.post("", response_model=MaintenanceRead, status_code=201, summary="Create maintenance")
async def create_maintenance(
    payload: MaintenanceCreate,
    session: AsyncSession = Depends(get_session),
    current: User = Depends(get_current_user),
) -> MaintenanceRead:
    m = await service.create(session, owner_id=current.id, payload=payload)
    if not m:
        raise HTTPException(status_code=404, detail="Bike not found or not owned by user")
    return MaintenanceRead.model_validate(m.__dict__)


@router.get("/{maintenance_id}", response_model=MaintenanceRead, summary="Get maintenance")
async def get_maintenance(
    maintenance_id: int,
    session: AsyncSession = Depends(get_session),
    current: User = Depends(get_current_user),
) -> MaintenanceRead:
    m = await service.get_for_user(session, owner_id=current.id, maintenance_id=maintenance_id)
    if not m:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return MaintenanceRead.model_validate(m.__dict__)


@router.put("/{maintenance_id}", response_model=MaintenanceRead, summary="Update maintenance")
async def update_maintenance(
    maintenance_id: int,
    payload: MaintenanceUpdate,
    session: AsyncSession = Depends(get_session),
    current: User = Depends(get_current_user),
) -> MaintenanceRead:
    m = await service.update(
        session, owner_id=current.id, maintenance_id=maintenance_id, payload=payload
    )
    if not m:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return MaintenanceRead.model_validate(m.__dict__)


@router.delete("/{maintenance_id}", status_code=204, summary="Delete maintenance")
async def delete_maintenance(
    maintenance_id: int,
    session: AsyncSession = Depends(get_session),
    current: User = Depends(get_current_user),
) -> None:
    ok = await service.delete(session, owner_id=current.id, maintenance_id=maintenance_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Maintenance not found")
