from typing import Optional

from pydantic_extra_types.epoch import Integer
from sqlalchemy import String, Column
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column




class Equipment(Base):
	__tablename__ = 'equipments'

	name: Mapped[str] = mapped_column(String(30))
	price: Mapped[int]
	category: Mapped[str] = mapped_column(String(30))