from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, condecimal

class MaintenanceBase(BaseModel):
    bike_id: int                                          # Lookup aufs Bike
    performed_at: datetime                                # Zeitpunkt (ISO 8601)
    is_external: bool                                     # extern vs. selbst
    description: Optional[str] = None
    vendor: Optional[str] = Field(default=None, max_length=200)
    cost: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    mileage_km: Optional[int] = Field(default=None, ge=0)
    duration_min: Optional[int] = Field(default=None, ge=0)
    warranty: Optional[bool] = None

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(BaseModel):
    performed_at: Optional[datetime] = None
    is_external: Optional[bool] = None
    description: Optional[str] = None
    vendor: Optional[str] = Field(default=None, max_length=200)
    cost: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    mileage_km: Optional[int] = Field(default=None, ge=0)
    duration_min: Optional[int] = Field(default=None, ge=0)
    warranty: Optional[bool] = None

class MaintenanceRead(MaintenanceBase):
    id: int
    created_at: datetime
    updated_at: datetime
