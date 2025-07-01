from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    account: str
    email: EmailStr
    avatar: Optional[str] = None
    real_name: Optional[str] = None
    organization: Optional[str] = None
    address: Optional[str] = None
    mobile: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True
