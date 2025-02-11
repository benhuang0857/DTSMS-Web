from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, EmailStr

# --- Login Schemas ---
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: str
    avatar: Optional[str] = None
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
    user_id: Optional[int] = None  # 指向 User 的外鍵
    token: Optional[str] = None
    status: Optional[str] = 'process'

class FileUploadCreate(FileUploadBase):
    pass  # 创建时与基本模式相同

class FileUploadUpdate(BaseModel):
    tracking_num: Optional[str] = None
    user_id: Optional[int] = None  # 支持更新 user_id
    token: Optional[str] = None
    status: Optional[str] = None

class FileUpload(FileUploadBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True

# --- Log Schemas ---
class LogBase(BaseModel):
    level: str
    message: str

class LogCreate(LogBase):
    pass

class LogUpdate(BaseModel):
    level: Optional[str] = None
    message: Optional[str] = None

class Log(LogBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True

# --- Reports  Schemas ---
class ReportBase(BaseModel):
    file_upload_id: int
    user_id: Optional[int] = None
    result: Optional[Dict] = None  # 假设 result 是 JSON 格式
    token: Optional[str] = None
    status: Optional[str] = 'process'

class ReportCreate(ReportBase):
    pass  # 创建时直接复用基础模型

class ReportUpdate(BaseModel):
    result: Optional[Dict] = None
    status: Optional[str] = None

class Report(ReportBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True  # 或 from_attributes=True 取决于 Pydantic 版本

# --- Role Schemas ---
class RoleBase(BaseModel):
    title: str
    status: Optional[str] = "active"
    note: Optional[str] = "active"

class RoleCreate(RoleBase):
    pass  # 创建时与基础模式一致

class RoleUpdate(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None

class Role(RoleBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True  # 如果是 Pydantic v2，请替换为 from_attributes = True

# --- Automations Schemas ---
class AutomationBase(BaseModel):
    user_id: Optional[int] = None
    note: Optional[str] = "active"
    status: Optional[str] = "process"

# Schema for creating automations
class AutomationCreate(AutomationBase):
    pass

# Schema for updating automations
class AutomationUpdate(BaseModel):
    note: Optional[str] = None
    status: Optional[str] = None

# Schema for returning automation data
class Automation(AutomationBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True

# --- Actions Schemas ---
class ActionBase(BaseModel):
    automation_id: Optional[int] = None
    api_type: Optional[str] = None
    endpoint: Optional[str] = None
    command: Optional[Dict[str, Any]] = None
    note: Optional[str] = "active"
    status: Optional[str] = "process"

# Schema for creating actions
class ActionCreate(ActionBase):
    pass

# Schema for updating actions
class ActionUpdate(BaseModel):
    api_type: Optional[str] = None
    endpoint: Optional[str] = None
    command: Optional[Dict[str, Any]] = None
    note: Optional[str] = None
    status: Optional[str] = None

# Schema for returning action data
class Action(ActionBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True
