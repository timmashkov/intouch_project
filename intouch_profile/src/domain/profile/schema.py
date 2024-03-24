from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GetProfileById(BaseModel):
    id: UUID


class GetProfileByFirstName(BaseModel):
    first_name: str


class GetProfileByLastName(BaseModel):
    last_name: str


class CreateUpdateProfile(GetProfileByLastName, GetProfileByFirstName):
    occupation: str | None
    status: str | None
    bio: str | None


class ProfileReturn(CreateUpdateProfile, GetProfileById):
    is_active: bool
    created_at: datetime
