from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt  # PyJWT
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(sub: str | int, minutes: int | None = None) -> str:
    exp_min = minutes or settings.JWT_EXPIRES_MIN
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(sub),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=exp_min)).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
