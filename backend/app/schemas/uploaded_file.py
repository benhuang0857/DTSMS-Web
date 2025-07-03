from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enums import TrackingStatus


# ✅ 表單輸入基礎
class UploadedFileBase(BaseModel):
    ticket_id: int
    unzip_password: Optional[str] = None
    description: Optional[str] = None


# ✅ 創建檔案時 (配合檔案上傳)
class UploadedFileCreate(UploadedFileBase):
    # name, ftype, fsize 由服務端根據 uploaded_file 決定
    pass


# ✅ 更新檔案 (全 optional)
class UploadedFileUpdate(BaseModel):
    name: Optional[str] = None
    ftype: Optional[str] = None
    fsize: Optional[int] = None
    unzip_password: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TrackingStatus] = None


# ✅ 響應模型
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
        orm_mode = True
