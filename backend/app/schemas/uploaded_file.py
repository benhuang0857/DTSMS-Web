from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 基礎 Schema
class UploadedFileBase(BaseModel):
    name: str
    file_type: str
    file_size: int
    destination: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

# 創建檔案
class UploadedFileCreate(UploadedFileBase):
    pass

# 更新檔案
class UploadedFileUpdate(UploadedFileBase):
    name: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None

# 響應檔案
class UploadedFile(UploadedFileBase):
    id: int
    user_id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True
