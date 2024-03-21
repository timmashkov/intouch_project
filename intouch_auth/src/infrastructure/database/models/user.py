from datetime import datetime

from sqlalchemy import String, Text, Boolean, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from intouch_auth.src.infrastructure.database.models.base import Base


class User(Base):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    token: Mapped[str] = mapped_column(
        Text, unique=False, nullable=True, server_default="", default=""
    )
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
