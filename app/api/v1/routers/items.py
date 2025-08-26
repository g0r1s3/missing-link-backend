# app/api/v1/routers/items.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.item import ItemCreate, ItemRead
from app.services import items as service

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=List[ItemRead], summary="List items")
def list_items(
    q: str | None = Query(default=None, description="Filter by name contains"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return service.list_items(q=q, limit=limit, offset=offset)

@router.post("", response_model=ItemRead, status_code=201, summary="Create item")
def create_item(payload: ItemCreate):
    return service.create_item(payload)

@router.get("/{item_id}", response_model=ItemRead, summary="Get one item")
def get_item(item_id: int):
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemRead, summary="Update item")
def update_item(item_id: int, payload: ItemCreate):
    updated = service.update_item(item_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}", status_code=204, summary="Delete item")
def delete_item(item_id: int):
    deleted = service.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
