from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enums import TrackingStatus
import uuid

class UploadedFileBase(BaseModel):
    ticket_id: int
    unzip_password: Optional[str] = None
    description: Optional[str] = None

class UploadedFileCreate(UploadedFileBase):
    # name, ftype, fsize 由服務端根據 uploaded_file 決定
    pass

class UploadedFileUpdate(BaseModel):
    name: Optional[str] = None
    ftype: Optional[str] = None
    fsize: Optional[int] = None
    unzip_password: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TrackingStatus] = None

class UploadedFile(BaseModel):
    id: int
    user_id: int
    ticket_id: Optional[int] = None
    name: str
    ftype: str
    fsize: int
    unzip_password: Optional[str] = None
    description: Optional[str] = None
    status: TrackingStatus
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True

class UploadedFileWithTracking(BaseModel):
    id: int
    user_id: int
    ticket_id: Optional[int] = None
    name: str
    ftype: str
    fsize: int
    unzip_password: Optional[str] = None
    description: Optional[str] = None
    status: TrackingStatus
    created_time: datetime
    updated_time: datetime
    tracking_id: Optional[uuid.UUID] = None
    step_name: Optional[str] = None
    start_time: Optional[datetime] = None

    class Config:
        from_attributes = True
