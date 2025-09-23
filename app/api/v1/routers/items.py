# app/api/v1/routers/items.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user  # neu
from app.db.session import get_session
from app.models.user import User  # neu
from app.schemas.item import ItemCreate, ItemRead
from app.services import items as service

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead], summary="List items")
async def list_items(
    q: str | None = Query(default=None, description="Filter by name contains"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> list[ItemRead]:
    items = await service.list_items(session, q=q, limit=limit, offset=offset)
    # in Schemas gießen (robust, falls Service DB-Modelle zurückgibt)
    return [ItemRead.model_validate(i.__dict__) for i in items]


@router.get("/{item_id}", response_model=ItemRead, summary="Get one item")
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)) -> ItemRead:
    item = await service.get_item(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemRead.model_validate(item.__dict__)


@router.post("", response_model=ItemRead, status_code=201, summary="Create item")
async def create_item(
    payload: ItemCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),  # geschützt
) -> ItemRead:
    created = await service.create_item(session, payload)
    return ItemRead.model_validate(created.__dict__)


@router.put("/{item_id}", response_model=ItemRead, summary="Update item")
async def update_item(
    item_id: int,
    payload: ItemCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),  # geschützt
) -> ItemRead:
    updated = await service.update_item(session, item_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemRead.model_validate(updated.__dict__)


@router.delete("/{item_id}", status_code=204, summary="Delete item")
async def delete_item(
    item_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),  # geschützt
) -> None:
    deleted = await service.delete_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
