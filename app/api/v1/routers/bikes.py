from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.db.session import get_session
from app.schemas.bike import BikeCreate, BikeUpdate, BikeRead
from app.services import bikes as service
from app.models.user import User

router = APIRouter(prefix="/bikes", tags=["bikes"])

@router.get("", response_model=List[BikeRead], summary="List my bikes")
async def list_my_bikes(
    q: str | None = Query(default=None, description="Filter by brand/model contains"),
    session: AsyncSession = Depends(get_session),
    current: User = Depends(get_current_user),
):
    bikes = await service.list_bikes(session, owner_id=current.id, q=q)
    return [BikeRead.model_validate(b.__dict__) for b in bikes]

@router.post("", response_model=BikeRead, status_code=201, summary="Create a bike")
async def create_my_bike(
    payload: BikeCreate,
    session: AsyncSession = Depends(get_session),
    current: User = Depends(get_current_user),
):
    bike = await service.create_bike(session, owner_id=current.id, payload=payload)
    return BikeRead.model_validate(bike.__dict__)

@router.get("/{bike_id}", response_model=BikeRead, summary="Get my bike")
async def get_my_bike(
    bike_id: int,
    session: AsyncSession = Depends(get_session),
    current: User = Depends(get_current_user),
):
    bike = await service.get_bike(session, owner_id=current.id, bike_id=bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    return BikeRead.model_validate(bike.__dict__)

@router.put("/{bike_id}", response_model=BikeRead, summary="Update my bike")
async def update_my_bike(
    bike_id: int,
    payload: BikeUpdate,
    session: AsyncSession = Depends(get_session),
    current: User = Depends(get_current_user),
):
    bike = await service.update_bike(session, owner_id=current.id, bike_id=bike_id, payload=payload)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    return BikeRead.model_validate(bike.__dict__)

@router.delete("/{bike_id}", status_code=204, summary="Delete my bike")
async def delete_my_bike(
    bike_id: int,
    session: AsyncSession = Depends(get_session),
    current: User = Depends(get_current_user),
):
    ok = await service.delete_bike(session, owner_id=current.id, bike_id=bike_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Bike not found")
