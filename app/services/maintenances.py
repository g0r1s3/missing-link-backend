from collections.abc import Sequence

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bike import Bike
from app.models.maintenance import Maintenance
from app.schemas.maintenance import MaintenanceCreate, MaintenanceUpdate


async def _ensure_bike_owned(session: AsyncSession, bike_id: int, owner_id: int) -> bool:
    q = await session.execute(
        select(Bike.id).where(and_(Bike.id == bike_id, Bike.owner_id == owner_id))
    )
    return q.scalar_one_or_none() is not None


async def list_for_user(
    session: AsyncSession, owner_id: int, bike_id: int | None = None
) -> Sequence[Maintenance]:
    stmt = (
        select(Maintenance)
        .join(Bike, Maintenance.bike_id == Bike.id)
        .where(Bike.owner_id == owner_id)
    )
    if bike_id is not None:
        stmt = stmt.where(Maintenance.bike_id == bike_id)
    stmt = stmt.order_by(Maintenance.performed_at.desc(), Maintenance.id.desc())
    res = await session.execute(stmt)
    return res.scalars().all()


async def get_for_user(
    session: AsyncSession, owner_id: int, maintenance_id: int
) -> Maintenance | None:
    stmt = (
        select(Maintenance)
        .join(Bike, Maintenance.bike_id == Bike.id)
        .where(Maintenance.id == maintenance_id, Bike.owner_id == owner_id)
    )
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def create(
    session: AsyncSession, owner_id: int, payload: MaintenanceCreate
) -> Maintenance | None:
    if not await _ensure_bike_owned(session, payload.bike_id, owner_id):
        return None
    m = Maintenance(**payload.model_dump())
    session.add(m)
    await session.commit()
    await session.refresh(m)
    return m


async def update(
    session: AsyncSession, owner_id: int, maintenance_id: int, payload: MaintenanceUpdate
) -> Maintenance | None:
    m = await get_for_user(session, owner_id, maintenance_id)
    if not m:
        return None
    data = payload.model_dump(exclude_unset=True)
    # bike_id darf NICHT „umgehängt“ werden - falls du erlauben willst, erst ownership prüfen
    if "bike_id" in data:
        data.pop("bike_id")
    for k, v in data.items():
        setattr(m, k, v)
    await session.commit()
    await session.refresh(m)
    return m


async def delete(session: AsyncSession, owner_id: int, maintenance_id: int) -> bool:
    m = await get_for_user(session, owner_id, maintenance_id)
    if not m:
        return False
    await session.delete(m)
    await session.commit()
    return True
