from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, AfterValidator
from typing_extensions import Annotated
from config import settings


def role_in_allowed_roles(role: str) -> str:
    """Ensures role are allowed"""
    assert role in settings.allowed_roles
    return role


class UserModel(BaseModel):
    username: str = Field(min_length=1, max_length=16)
    email: EmailStr
    password: str = Field(min_length=1, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    role: Annotated[str, AfterValidator(role_in_allowed_roles)]

    class Config:
        # orm_mode = True
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ChangePassword(BaseModel):
    old_password: str = Field(min_length=6, max_length=10)
    new_password: str = Field(min_length=6, max_length=10)


class EmailModel(BaseModel):
    email: EmailStr
