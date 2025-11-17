from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import equipment_services
from app.services import equipment_services
from app.db.db import get_db
from app.schemas.equipment_schemas import EquipmentSchema, EquipmentCreate


router = APIRouter(
    tags=["Equipment"],
    prefix="/equipment",
)


@router.get("/{equipment_id}")
async def read_equipment(equipment_id: int, db: AsyncSession = Depends(get_db)):
    equipment = await equipment_services.read_equipment(equipment_id=equipment_id,db=db)
    return equipment


@router.post("/")
async def create_equipment(equipment: EquipmentCreate,db: AsyncSession = Depends(get_db)):
    new_equipment = await equipment_services.create_equipment(
        name=equipment.name,
        category=equipment.category,
        price=equipment.price,
        db=db
    )
    return new_equipment


@router.patch("/{equipment_id}")
async def update_equipment(
        equipment_id: int,
        name: str | None = Query(default=None, max_length=30),
        category: str | None = Query(default=None, max_length=30),
        price: int | None = None,
        db: AsyncSession = Depends(get_db)
):
    updated_equipment = await equipment_services.update_equipment(
        equipment_id=equipment_id,
        name=name,
        category=category,
        price=price,
        db=db
    )
    return updated_equipment


@router.delete("/{equipment_id}")
async def delete_equipment(equipment_id: int, db: AsyncSession = Depends(get_db)):
    deleted_equipment = await equipment_services.delete_equipment(equipment_id=equipment_id,db=db)
    return deleted_equipment