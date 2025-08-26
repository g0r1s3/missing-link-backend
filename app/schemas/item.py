# app/schemas/item.py
from pydantic import BaseModel, Field
from typing import Optional

class ItemCreate(BaseModel):
    """Eingabe-Schema fürs Erstellen/Aktualisieren."""
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None

class ItemRead(ItemCreate):
    """Ausgabe-Schema mit vergebener ID."""
    id: int
