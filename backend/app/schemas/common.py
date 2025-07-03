from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enums import BasicStatus
from schemas.role import Role

class UserSummary(BaseModel):
    id: int
    role: Optional[Role] = None
    account: str
    email: EmailStr
    avatar: Optional[str] = None
    real_name: Optional[str] = None
    organization: Optional[str] = None
    address: Optional[str] = None
    mobile: Optional[str] = None
    status: BasicStatus

    class Config:
        from_attributes = True

class TicketSummary(BaseModel):
    id: int
    code: str
    exp_start_time: Optional[datetime] = None
    exp_end_time: Optional[datetime] = None
    status: BasicStatus
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True
