from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enums import BasicStatus

class TicketBase(BaseModel):
    ticket_num: str
    status: BasicStatus

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    ticket_num: Optional[str] = None
    status: Optional[BasicStatus] = None

class Ticket(TicketBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True
