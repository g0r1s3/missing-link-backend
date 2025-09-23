# app/core/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_session
from app.models.user import User
from app.services import users as users_service

# WICHTIG: auto_error=False, damit wir selbst 401 zurückgeben können
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    # Kein/leerere Header -> 401
    if creds is None or not getattr(creds, "credentials", None):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = creds.credentials
    try:
        payload = decode_token(token)
    except Exception as err:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from err

    sub = payload.get("sub")
    if not isinstance(sub, str | int):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = int(sub)

    user = await users_service.get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
