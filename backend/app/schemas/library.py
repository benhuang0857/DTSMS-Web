from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enums import BasicStatus

class LibraryBase(BaseModel):
    name: str
    protocal: Optional[str] = None
    baudrate: Optional[int] = None
    parity: Optional[str] = None
    stopbits: Optional[int] = None
    bytesize: Optional[int] = None
    host: Optional[str] = None
    port: Optional[int] = None
    certfile: Optional[str] = None
    description: Optional[str] = None
    status: BasicStatus

class LibraryCreate(LibraryBase):
    pass

class LibraryUpdate(BaseModel):
    name: Optional[str] = None
    protocal: Optional[str] = None
    baudrate: Optional[int] = None
    parity: Optional[str] = None
    stopbits: Optional[int] = None
    bytesize: Optional[int] = None
    host: Optional[str] = None
    port: Optional[int] = None
    certfile: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BasicStatus] = None

class Library(LibraryBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True
