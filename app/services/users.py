# app/services/users.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate  # <- neu


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    res = await session.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()


async def register_user(session: AsyncSession, email: str, password: str) -> User:
    exists = await get_user_by_email(session, email)
    if exists:
        raise ValueError("email_taken")
    user = User(email=email, password_hash=hash_password(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate(session: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def get_by_id(session: AsyncSession, user_id: int) -> User | None:
    res = await session.execute(select(User).where(User.id == user_id))
    return res.scalar_one_or_none()


# ---- Kompatibilitäts-Wrapper: akzeptiert UserCreate ODER email/password ----
async def register(
    session: AsyncSession,
    payload: UserCreate | None = None,
    email: str | None = None,
    password: str | None = None,
) -> User:
    """
    Akzeptiert entweder:
      - register(session, UserCreate(...))
      - register(session, email="...", password="...")
    """
    if payload is not None:
        email = payload.email
        password = payload.password
    if not email or not password:
        raise TypeError(
            "register() requires either 'payload' (UserCreate) or both 'email' and 'password'"
        )
    return await register_user(session, email, password)
