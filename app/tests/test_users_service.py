import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate
from app.services import users as user_service

pytestmark = pytest.mark.anyio("asyncio")


async def test_register_and_authenticate(db_session: AsyncSession) -> None:
    u = await user_service.register(
        db_session, UserCreate(email="zoe@example.com", password="secret123")
    )
    assert u.email == "zoe@example.com"
    user = await user_service.authenticate(db_session, "zoe@example.com", "secret123")
    assert user is not None
    bad = await user_service.authenticate(db_session, "zoe@example.com", "WRONG")
    assert bad is None
