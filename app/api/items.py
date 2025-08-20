from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.item import Item

router = APIRouter(prefix="/items", tags=["items"])

# einfache In-Memory "DB"
items: List[Item] = []

@router.get("", response_model=List[Item])
def list_items():
    return items

@router.post("", response_model=Item, status_code=201)
def create_item(item: Item):
    if any(i.id == item.id for i in items):
        raise HTTPException(status_code=400, detail="ID already exists")
    items.append(item)
    return item
