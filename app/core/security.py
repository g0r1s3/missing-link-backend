# app/core/security.py
from datetime import UTC, datetime, timedelta

import jwt  # PyJWT
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(sub: str | int) -> str:
    now = datetime.now(tz=UTC)
    exp = now + timedelta(minutes=settings.JWT_EXPIRES_MIN)
    payload = {"sub": str(sub), "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
