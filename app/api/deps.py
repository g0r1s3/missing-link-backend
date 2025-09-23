# app/api/deps.py
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_session
from app.models.user import User
from app.services import users as user_service


async def get_current_user(
    authorization: str | None = Header(default=None, alias="Authorization"),
    session: AsyncSession = Depends(get_session),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub") or 0)
    except Exception:
        # B904: explicit chaining - hier bewusst ohne Original-Traceback
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from None

    user = await user_service.get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
