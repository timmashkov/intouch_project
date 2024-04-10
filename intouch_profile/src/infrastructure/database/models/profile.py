from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Text,
    Boolean,
    func,
    UUID,
    Integer,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, column_property, relationship

from .base import Base

if TYPE_CHECKING:
    from .post import Post


class Friend(Base):
    __tablename__ = "friend"
    __table_args__ = (
        UniqueConstraint("profile_id", "friend_id", name="idx_unique_profile_friend"),
        {"extend_existing": True},
    )

    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profile.id"))
    friend_id: Mapped[UUID] = mapped_column(ForeignKey("profile.id"))


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
    #  From intouch_auth microservice
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False
    )
    #
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
    timeframe = column_property(func.now() - created_at)

    friends: Mapped[list["Profile"]] = relationship(
        "Profile",
        secondary="friend",
        primaryjoin="Profile.id==Friend.profile_id",
        secondaryjoin="Profile.id==Friend.friend_id",
    )

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
