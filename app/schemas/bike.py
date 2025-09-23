from datetime import date, datetime

from pydantic import BaseModel, Field


class BikeBase(BaseModel):
    brand: str = Field(min_length=1, max_length=120)
    model: str | None = Field(default=None, max_length=120)
    color: str | None = Field(default=None, max_length=60)
    year: int | None = Field(default=None, ge=1900, le=2100)
    frame_number: str | None = Field(default=None, max_length=120)
    purchase_date: date | None = None
    weight_kg: int | None = Field(default=None, ge=0, le=200)
    brake_type: str | None = Field(default=None, max_length=60)
    tire_size: str | None = Field(default=None, max_length=40)


class BikeCreate(BikeBase):
    pass


class BikeUpdate(BaseModel):
    brand: str | None = Field(default=None, min_length=1, max_length=120)
    model: str | None = Field(default=None, max_length=120)
    color: str | None = Field(default=None, max_length=60)
    year: int | None = Field(default=None, ge=1900, le=2100)
    frame_number: str | None = Field(default=None, max_length=120)
    purchase_date: date | None = None
    weight_kg: int | None = Field(default=None, ge=0, le=200)
    brake_type: str | None = Field(default=None, max_length=60)
    tire_size: str | None = Field(default=None, max_length=40)


class BikeRead(BikeBase):
    id: int
    created_at: datetime
    updated_at: datetime
