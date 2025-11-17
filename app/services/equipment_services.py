from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.equipment_model import Equipment


async def create_equipment(name: str, category: str, price: int, db: AsyncSession):
    new_equipment = Equipment(
        name=name,
        category=category,
        price=price
    )
    db.add(new_equipment)
    await db.commit()
    await db.refresh(new_equipment)
    return new_equipment


async def read_equipment(equipment_id: int, db: AsyncSession):
    query = select(Equipment).where(Equipment.id == equipment_id)
    result = await db.execute(query)
    equipment_info = result.scalar_one_or_none()
    if equipment_info is None:
        raise HTTPException(status_code=404, detail='Equipment not found')
    return equipment_info


async def update_equipment(
        equipment_id: int,
        db: AsyncSession,
        name: str | None = None,
        category: str | None = None,
        price: int | None = None
):
    equipment_to_update = await read_equipment(equipment_id, db)

    if name is not None:
        equipment_to_update.name = name
    if category is not None:
        equipment_to_update.category = category
    if price is not None:
        equipment_to_update.price = price
    if name is None and category is None and price is None:
        raise HTTPException(status_code=400, detail='You need to specify at least one field')

    await db.commit()
    await db.refresh(equipment_to_update)
    return equipment_to_update


async def delete_equipment(equipment_id: int, db: AsyncSession):
    equipment_to_delete = await read_equipment(equipment_id, db)
    await db.delete(equipment_to_delete)
    await db.commit()
    return {"msg": "Equipment deleted"}