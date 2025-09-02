from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token
from app.services import users as user_service
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await user_service.get_by_email(session, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return await user_service.register(session, payload)

@router.post("/login", response_model=Token)
async def login(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await user_service.authenticate(session, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(sub=user.id)
    return {"access_token": token, "token_type": "bearer"}
