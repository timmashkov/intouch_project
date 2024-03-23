from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class GetUserById(BaseModel):
    id: UUID | str


class GetUserByLogin(BaseModel):
    login: str


class UpdateUser(GetUserByLogin):
    email: EmailStr
    age: int
    phone_number: str = Field(examples=["89986661488", "+79986661488"])

    @field_validator("age")
    def check_age(cls, value):
        if 1 <= value <= 100:
            return value
        raise ValueError("Age must be higher then 0 and less then 101")

    @field_validator("phone_number")
    def check_number(cls, value):
        if (value.isdigit() and len(value) == 11) or (
            value[1:].isdigit() and value.startswith("+") and len(value) == 12
        ):
            return value
        raise ValueError("Invalid phone number")


class CreateUser(UpdateUser):
    password: str


class UserReturnData(GetUserById, GetUserByLogin):
    email: EmailStr
    age: int
    phone_number: str = Field(examples=["89986661488", "+79986661488"])
    is_verified: bool
    registered_at: datetime


class UserSecretData(GetUserById, GetUserByLogin):
    password: str
    email: EmailStr


class UserLogin(GetUserByLogin):
    password: str


class UserJwtToken(GetUserById):
    token: str


class UserAccessToken(BaseModel):
    access_token: str
