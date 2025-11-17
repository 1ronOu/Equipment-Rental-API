from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query


class EquipmentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(max_length=30)
    price: int
    category: str = Field(max_length=30)


class EquipmentCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(max_length=30)
    price: int
    category: str = Field(max_length=30)
