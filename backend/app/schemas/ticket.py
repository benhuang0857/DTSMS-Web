from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enums import BasicStatus
from schemas.common import UserSummary

class TicketBase(BaseModel):
    code: str

class TicketCreate(TicketBase):
    user_id: Optional[int] = None
    exp_start_time: Optional[datetime] = None
    exp_end_time: Optional[datetime] = None
    status: Optional[BasicStatus] = None

class TicketUpdate(BaseModel):
    user_id: Optional[int] = None
    exp_start_time: Optional[datetime] = None
    exp_end_time: Optional[datetime] = None
    status: Optional[BasicStatus] = None

class Ticket(TicketBase):
    id: int
    user: Optional[UserSummary] = None
    exp_start_time: Optional[datetime] = None
    exp_end_time: Optional[datetime] = None
    status: BasicStatus
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True
