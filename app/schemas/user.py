from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str | None = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None

class UserRead(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True