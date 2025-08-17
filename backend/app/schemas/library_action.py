from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from enums import BasicStatus

class LibraryActionBase(BaseModel):
    name: str
    api_path: str
    http_method: str = "POST"
    request_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    execution_order: Optional[int] = None
    status: BasicStatus = BasicStatus.active

class LibraryActionCreate(LibraryActionBase):
    library_id: int

class LibraryActionUpdate(BaseModel):
    name: Optional[str] = None
    api_path: Optional[str] = None
    http_method: Optional[str] = None
    request_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    execution_order: Optional[int] = None
    status: Optional[BasicStatus] = None

class LibraryAction(LibraryActionBase):
    id: int
    library_id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True