# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
