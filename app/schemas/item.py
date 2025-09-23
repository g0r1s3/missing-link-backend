# app/schemas/item.py

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """Eingabe-Schema fürs Erstellen/Aktualisieren."""

    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class ItemRead(ItemCreate):
    """Ausgabe-Schema mit vergebener ID."""

    id: int
