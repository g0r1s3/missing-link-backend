# app/api/v1/routers/auth.py
from datetime import datetime
from typing import cast

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.security import create_access_token
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services import users as users_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    # users_service.create_user gibt es nicht -> register_user verwenden
    user = await users_service.register_user(session, payload.email, payload.password)
    return UserRead(
        id=user.id,
        email=user.email,
        created_at=cast(datetime, user.created_at),
    )


@router.post("/login")
async def login(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    user = await users_service.authenticate(session, payload.email, payload.password)
    if not user:
        # HTTPException ist jetzt korrekt importiert
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(sub=str(user.id))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def me(current: User = Depends(get_current_user)) -> UserRead:
    return UserRead(
        id=current.id,
        email=current.email,
        created_at=cast(datetime, current.created_at),
    )
