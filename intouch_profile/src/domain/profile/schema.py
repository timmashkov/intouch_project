from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


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
    login: str
    email: EmailStr
    age: int
    phone_number: str
    registered_at: datetime | str
    user_id: UUID | str


class ProfileReturn(CreateProfile, GetProfileById):
    is_active: bool
    created_at: datetime
