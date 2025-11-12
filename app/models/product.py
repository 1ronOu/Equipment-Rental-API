from typing import Optional
from sqlalchemy import String
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
	__tablename__ = 'products'

	name: Mapped[str] = mapped_column(String(30))
	price: Mapped[Optional[int]]
	desription: Mapped[str] = mapped_column(String(30))