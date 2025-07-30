from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enums import BasicStatus
from schemas.role import Role
from schemas.common import TicketSummary

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
    role_id: int
    password: str

class UserUpdate(BaseModel):
    account: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    real_name: Optional[str] = None
    organization: Optional[str] = None
    address: Optional[str] = None
    mobile: Optional[str] = None
    status: Optional[BasicStatus] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    role: Optional[Role] = None
    # tickets: List[TicketSummary] = []
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True
