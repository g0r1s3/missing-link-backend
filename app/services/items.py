from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemRead


async def list_items(
    session: AsyncSession, q: str | None = None, limit: int = 20, offset: int = 0
) -> list[ItemRead]:
    stmt = select(Item)
    if q:
        stmt = stmt.where(Item.name.ilike(f"%{q}%"))
    stmt = stmt.offset(offset).limit(limit)
    result = await session.execute(stmt)
    items = result.scalars().all()
    return [ItemRead.model_validate(i.__dict__) for i in items]


async def create_item(session: AsyncSession, payload: ItemCreate) -> ItemRead:
    new_item = Item(name=payload.name, description=payload.description)
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return ItemRead.model_validate(new_item.__dict__)


async def get_item(session: AsyncSession, item_id: int) -> ItemRead | None:
    stmt = select(Item).where(Item.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()
    if item:
        return ItemRead.model_validate(item.__dict__)
    return None


async def update_item(session: AsyncSession, item_id: int, payload: ItemCreate) -> ItemRead | None:
    stmt = select(Item).where(Item.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()
    if not item:
        return None
    item.name = payload.name
    item.description = payload.description
    await session.commit()
    await session.refresh(item)
    return ItemRead.model_validate(item.__dict__)


async def delete_item(session: AsyncSession, item_id: int) -> bool:
    stmt = select(Item).where(Item.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()
    if not item:
        return False
    await session.delete(item)
    await session.commit()
    return True
