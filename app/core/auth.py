# app/core/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_session
from app.services import users as users_service
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=True)

async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    token = creds.credentials
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if not sub:
            raise ValueError("no-sub")
        user_id = int(sub)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await users_service.get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

