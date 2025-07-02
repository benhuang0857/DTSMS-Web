from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enums import TrackingStatus

# 基礎 Schema
class UploadedFileBase(BaseModel):
    name: str
    ticket_num: str
    ftype: str
    fsize: int
    unzip_password: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TrackingStatus] = None

# 創建檔案
class UploadedFileCreate(UploadedFileBase):
    pass

# 更新檔案
class UploadedFileUpdate(UploadedFileBase):
    name: Optional[str] = None
    ftype: Optional[str] = None
    fsize: Optional[int] = None
    status: Optional[TrackingStatus] = None

# 響應檔案
class UploadedFile(UploadedFileBase):
    id: int
    user_id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True
