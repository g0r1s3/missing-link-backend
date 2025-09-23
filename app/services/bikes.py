from collections.abc import Sequence

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bike import Bike
from app.schemas.bike import BikeCreate, BikeUpdate


async def list_bikes(session: AsyncSession, owner_id: int, q: str | None = None) -> Sequence[Bike]:
    stmt = select(Bike).where(Bike.owner_id == owner_id).order_by(Bike.created_at.desc())
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            and_(Bike.owner_id == owner_id, (Bike.brand.ilike(like) | (Bike.model.ilike(like))))
        )
    res = await session.execute(stmt)
    return res.scalars().all()


async def get_bike(session: AsyncSession, owner_id: int, bike_id: int) -> Bike | None:
    res = await session.execute(select(Bike).where(Bike.id == bike_id, Bike.owner_id == owner_id))
    return res.scalar_one_or_none()


async def create_bike(session: AsyncSession, owner_id: int, payload: BikeCreate) -> Bike:
    bike = Bike(owner_id=owner_id, **payload.model_dump(exclude_unset=True))
    session.add(bike)
    await session.commit()
    await session.refresh(bike)
    return bike


async def update_bike(
    session: AsyncSession, owner_id: int, bike_id: int, payload: BikeUpdate
) -> Bike | None:
    bike = await get_bike(session, owner_id, bike_id)
    if not bike:
        return None
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(bike, k, v)
    await session.commit()
    await session.refresh(bike)
    return bike


async def delete_bike(session: AsyncSession, owner_id: int, bike_id: int) -> bool:
    bike = await get_bike(session, owner_id, bike_id)
    if not bike:
        return False
    await session.delete(bike)
    await session.commit()
    return True
