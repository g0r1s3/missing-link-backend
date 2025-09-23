# app/schemas/user.py
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
