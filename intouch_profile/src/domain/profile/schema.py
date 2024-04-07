from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, model_validator


class GetProfileById(BaseModel):
    id: UUID


class GetProfileByFirstName(BaseModel):
    first_name: str = ""


class GetProfileByLastName(BaseModel):
    last_name: str = ""


class UpdateProfile(GetProfileByLastName, GetProfileByFirstName):
    occupation: str | None
    status: str | None
    bio: str | None


class CreateProfile(UpdateProfile):
    first_name: str = ""
    last_name: str = ""
    email: EmailStr
    age: int
    phone_number: str
    occupation: str | None
    status: str | None
    bio: str | None
    user_id: UUID | str


class ProfileReturn(CreateProfile, GetProfileById):
    is_active: bool
    created_at: datetime


class FriendSchema(BaseModel):
    profile_id: UUID
    friend_id: UUID

    @model_validator(mode="before")
    def check_ids_not_equal(cls, values):
        if values.get("profile_id") == values.get("friend_id"):
            raise ValueError("Profile ID and Friend ID cannot be the same")
        return values
