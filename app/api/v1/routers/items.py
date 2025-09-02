from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.item import ItemCreate, ItemRead
from app.services import items as service
from app.db.session import get_session
from app.api.deps import get_current_user  # schützt schreibende Endpunkte

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=List[ItemRead], summary="List items")
async def list_items(
    q: str | None = Query(default=None, description="Filter by name contains"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await service.list_items(session, q=q, limit=limit, offset=offset)

@router.get("/{item_id}", response_model=ItemRead, summary="Get one item")
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await service.get_item(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("", response_model=ItemRead, status_code=201, summary="Create item")
async def create_item(
    payload: ItemCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),  # geschützt
):
    return await service.create_item(session, payload)

@router.put("/{item_id}", response_model=ItemRead, summary="Update item")
async def update_item(
    item_id: int,
    payload: ItemCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),  # geschützt
):
    updated = await service.update_item(session, item_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}", status_code=204, summary="Delete item")
async def delete_item(
    item_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),  # geschützt
):
    deleted = await service.delete_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
