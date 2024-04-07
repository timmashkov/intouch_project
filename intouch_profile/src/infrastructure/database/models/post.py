from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, func, UUID, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .profile import Profile


class Post(Base):
    __tablename__ = "post"

    header: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    hashtag: Mapped[str] = mapped_column(String(30), unique=False, nullable=True)
    body: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    written_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("profile.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    author: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="posts",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
