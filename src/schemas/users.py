from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    username: str = Field(min_length=1, max_length=16)
    email: EmailStr
    password: str = Field(min_length=1, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    is_admin: bool
    is_moderator: bool
    is_banned: bool

    class Config:
        # orm_mode = True
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserProfileUpdate(BaseModel):
    username: str
    email: str


class UserProfileResponse(BaseModel):
    username: str
    created_at: datetime
