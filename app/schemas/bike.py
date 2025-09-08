from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class BikeBase(BaseModel):
    brand: str = Field(min_length=1, max_length=120)
    model: Optional[str] = Field(default=None, max_length=120)
    color: Optional[str] = Field(default=None, max_length=60)
    year: Optional[int] = Field(default=None, ge=1900, le=2100)
    frame_number: Optional[str] = Field(default=None, max_length=120)
    purchase_date: Optional[date] = None
    weight_kg: Optional[int] = Field(default=None, ge=0, le=200)
    brake_type: Optional[str] = Field(default=None, max_length=60)
    tire_size: Optional[str] = Field(default=None, max_length=40)

class BikeCreate(BikeBase):
    pass

class BikeUpdate(BaseModel):
    brand: Optional[str] = Field(default=None, min_length=1, max_length=120)
    model: Optional[str] = Field(default=None, max_length=120)
    color: Optional[str] = Field(default=None, max_length=60)
    year: Optional[int] = Field(default=None, ge=1900, le=2100)
    frame_number: Optional[str] = Field(default=None, max_length=120)
    purchase_date: Optional[date] = None
    weight_kg: Optional[int] = Field(default=None, ge=0, le=200)
    brake_type: Optional[str] = Field(default=None, max_length=60)
    tire_size: Optional[str] = Field(default=None, max_length=40)

class BikeRead(BikeBase):
    id: int
    created_at: datetime
    updated_at: datetime
