from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enums import TrackingStatus
import uuid

class FileTrackingBase(BaseModel):
    uploaded_file_id: int
    step_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    result: Optional[str] = None
    status: TrackingStatus
    note: Optional[str] = None

class FileTrackingCreate(FileTrackingBase):
    pass

class FileTrackingUpdate(BaseModel):
    step_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    result: Optional[str] = None
    status: Optional[TrackingStatus] = None
    note: Optional[str] = None

class FileTracking(FileTrackingBase):
    id: int
    tracking_id: uuid.UUID
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True

class FileTrackingWithRelations(BaseModel):
    id: int
    tracking_id: uuid.UUID
    uploaded_file_id: int
    step_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    result: Optional[str] = None
    status: TrackingStatus
    note: Optional[str] = None
    created_time: datetime
    updated_time: datetime
    
    # 關聯的資料
    uploaded_file_name: Optional[str] = None
    uploaded_file_status: Optional[TrackingStatus] = None
    step_name: Optional[str] = None
    step_description: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True