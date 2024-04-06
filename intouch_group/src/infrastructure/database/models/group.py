from datetime import datetime

from sqlalchemy import String, Boolean, Text, UUID, func
from sqlalchemy.orm import Mapped, mapped_column

from intouch_group.src.infrastructure.database.models.base import Base


class Group(Base):
    __tablename__ = "group"

    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    is_official: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    group_admin: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False
    )
