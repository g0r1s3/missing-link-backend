# app/tests/test_items_service.py
import pytest
from app.schemas.item import ItemCreate
from app.services import items as service
pytestmark = pytest.mark.anyio("asyncio")


async def test_create_and_get_item(db_session):
    created = await service.create_item(db_session, ItemCreate(name="Pumpe", description="Mini"))
    fetched = await service.get_item(db_session, created.id)
    assert fetched is not None
    assert fetched.name == "Pumpe"
    assert fetched.description == "Mini"

async def test_list_items_filter_and_pagination(db_session):
    await service.create_item(db_session, ItemCreate(name="Pumpe A"))
    await service.create_item(db_session, ItemCreate(name="Schlauch"))
    await service.create_item(db_session, ItemCreate(name="Pumpe B"))

    filtered = await service.list_items(db_session, q="pum")
    assert len(filtered) == 2

    all_items = await service.list_items(db_session)
    assert len(all_items) == 3
    assert len(await service.list_items(db_session, limit=1, offset=0)) == 1
    assert len(await service.list_items(db_session, limit=1, offset=1)) == 1

async def test_update_and_delete_item(db_session):
    created = await service.create_item(db_session, ItemCreate(name="Alt"))
    updated = await service.update_item(db_session, created.id, ItemCreate(name="Neu"))
    assert updated is not None
    assert updated.name == "Neu"

    deleted_ok = await service.delete_item(db_session, created.id)
    assert deleted_ok is True
    assert await service.get_item(db_session, created.id) is None

    assert await service.delete_item(db_session, 999_999) is False
