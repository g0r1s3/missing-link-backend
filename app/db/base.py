# app/db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# WICHTIG: Modelle importieren, damit Alembic sie „sieht“
from app.models.item import Item  # noqa: F401
