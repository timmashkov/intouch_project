import uuid
from datetime import datetime

from sqlalchemy import String, Text, Boolean, func, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Profile(Base):
    __tablename__ = "profile"

    first_name: Mapped[str] = mapped_column(
        String(20), unique=False, nullable=False, default=""
    )
    last_name: Mapped[str] = mapped_column(
        String(30), unique=False, nullable=False, default=""
    )
    occupation: Mapped[str] = mapped_column(String(30), unique=False, nullable=True)
    status: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    bio: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
