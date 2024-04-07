from datetime import datetime

from sqlalchemy import String, Text, Boolean, func, UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column, column_property, relationship

from .base import Base


class Post(Base):
    __tablename__ = "post"

    header: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    hashtag: Mapped[str] = mapped_column(String(30), unique=False, nullable=True)
    body: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    likes: Mapped[int] = mapped_column(Integer, default=0)
