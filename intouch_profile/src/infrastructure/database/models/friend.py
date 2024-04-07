from uuid import UUID
from sqlalchemy import ForeignKey, UniqueConstraint
from infrastructure.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Friend(Base):
    __tablename__ = "friend"
    __table_args__ = (
        UniqueConstraint("profile_id", "friend_id", name="idx_unique_profile_friend"),
    )

    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profile.id"))
    friend_id: Mapped[UUID] = mapped_column(ForeignKey("profile.id"))
