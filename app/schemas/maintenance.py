# app/schemas/maintenance.py
from datetime import datetime
from decimal import Decimal
from typing import Annotated, TypeAlias

from pydantic import BaseModel, Field

# Mypy- und Pydantic-v2-freundlicher Typ für Geldbeträge
Cost: TypeAlias = Annotated[Decimal, Field(max_digits=10, decimal_places=2)]  # noqa: UP040


class MaintenanceBase(BaseModel):
    bike_id: int  # Lookup aufs Bike
    performed_at: datetime  # Zeitpunkt (ISO 8601)
    is_external: bool  # extern vs. selbst
    description: str | None = None
    vendor: str | None = Field(default=None, max_length=200)
    cost: Cost | None = None
    mileage_km: int | None = Field(default=None, ge=0)
    duration_min: int | None = Field(default=None, ge=0)
    warranty: bool | None = None


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(BaseModel):
    performed_at: datetime | None = None
    is_external: bool | None = None
    description: str | None = None
    vendor: str | None = Field(default=None, max_length=200)
    cost: Cost | None = None
    mileage_km: int | None = Field(default=None, ge=0)
    duration_min: int | None = Field(default=None, ge=0)
    warranty: bool | None = None


class MaintenanceRead(MaintenanceBase):
    id: int
    created_at: datetime
    updated_at: datetime
