# app/api/v1/routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token
from app.services import users as users_service
from app.core.security import create_access_token
from app.db.session import get_session
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=201)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        user = await users_service.register_user(session, payload.email, payload.password)
    except ValueError as e:
        if str(e) == "email_taken":
            raise HTTPException(status_code=409, detail="Email already registered")
        raise
    return UserRead(id=user.id, email=user.email, created_at=user.created_at)

@router.post("/login", response_model=Token)
async def login(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await users_service.authenticate(session, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(sub=user.id)
    return Token(access_token=token)

@router.get("/me", response_model=UserRead)
async def me(current: User = Depends(get_current_user)):
    return UserRead(id=current.id, email=current.email, created_at=current.created_at)
