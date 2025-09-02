from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password, verify_password

async def get_by_email(session: AsyncSession, email: str) -> Optional[User]:
    res = await session.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()

async def get_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
    res = await session.execute(select(User).where(User.id == user_id))
    return res.scalar_one_or_none()

async def register(session: AsyncSession, payload: UserCreate) -> UserRead:
    user = User(email=payload.email, password_hash=hash_password(payload.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserRead.model_validate(user)

async def authenticate(session: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
