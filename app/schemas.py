from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: str
    real_name: Optional[str] = None
    organization: Optional[str] = None
    address: Optional[str] = None
    mobile: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int  # 返回的用户 ID
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True

# --- FileUpload Schemas ---
class FileUploadBase(BaseModel):
    tracking_num: str
    user: str
    token: Optional[str] = None
    status: Optional[str] = 'process'

class FileUploadCreate(FileUploadBase):
    pass  # 创建时与基本模式相同

class FileUploadUpdate(BaseModel):
    token: Optional[str] = None
    status: Optional[str] = None

class FileUpload(FileUploadBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True
