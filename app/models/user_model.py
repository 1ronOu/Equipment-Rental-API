from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
	__tablename__ = 'users'

	name: Mapped[str] = mapped_column(String(30))
	email: Mapped[str] = mapped_column(String(30))
	password: Mapped[str] = mapped_column(String(30))
