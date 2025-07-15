from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    username: str


class UserUpdate(BaseModel):
    username: str | None = None
    first_login: bool | None = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    first_login: bool

    class Config:
        from_attributes = True


class LoginData(BaseModel):
    username: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
