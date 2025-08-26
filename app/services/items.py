# app/services/items.py
from typing import Dict, List, Optional
from app.schemas.item import ItemCreate, ItemRead

# In-Memory-"Datenbank"
_DB: Dict[int, ItemRead] = {}
_counter = 0

def _next_id() -> int:
    global _counter
    _counter += 1
    return _counter

def list_items(q: Optional[str] = None, limit: int = 20, offset: int = 0) -> List[ItemRead]:
    """Items mit optionalem Filter (name enthält q), plus Pagination."""
    items = list(_DB.values())
    if q:
        q_lower = q.lower()
        items = [i for i in items if q_lower in i.name.lower()]
    return items[offset: offset + limit]

def create_item(payload: ItemCreate) -> ItemRead:
    """Neues Item anlegen und speichern."""
    new = ItemRead(id=_next_id(), **payload.model_dump())
    _DB[new.id] = new
    return new

def get_item(item_id: int) -> Optional[ItemRead]:
    """Ein Item lesen (oder None)."""
    return _DB.get(item_id)

def update_item(item_id: int, payload: ItemCreate) -> Optional[ItemRead]:
    """Item updaten; None, wenn es nicht existiert."""
    if item_id not in _DB:
        return None
    updated = ItemRead(id=item_id, **payload.model_dump())
    _DB[item_id] = updated
    return updated

def delete_item(item_id: int) -> bool:
    """Item löschen; True bei Erfolg, False wenn nicht vorhanden."""
    return _DB.pop(item_id, None) is not None
