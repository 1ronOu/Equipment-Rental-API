from typing import Optional
from sqlalchemy import String, Column
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column




class Equipment(Base):
	__tablename__ = 'equipments'

	name: Mapped[str] = mapped_column(String(30))
	price: Mapped[Optional[int]] = mapped_column(String(30))