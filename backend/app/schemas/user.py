from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enums import BasicStatus
from schemas.role import Role

class UserBase(BaseModel):
    account: str
    email: EmailStr
    avatar: Optional[str] = None
    real_name: Optional[str] = None
    organization: Optional[str] = None
    address: Optional[str] = None
    mobile: Optional[str] = None
    status: BasicStatus

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    avatar: Optional[str] = None
    real_name: Optional[str] = None
    organization: Optional[str] = None
    address: Optional[str] = None
    mobile: Optional[str] = None
    status: Optional[BasicStatus] = None

class User(UserBase):
    id: int
    role: Optional[Role] = None
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True
