from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str | None = None

class UserCreate(UserBase):
    password: str
    email: str | None = None

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None

class UserRead(UserBase):
    id: int
    created_at: datetime
    first_login : bool
    class Config:
        from_attributes = True
        
class LoginData(BaseModel):
    username: str
    password: str | None = None
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str