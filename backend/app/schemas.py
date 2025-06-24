from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# --- Login Schemas ---
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- User Schemas ---
class UserBase(BaseModel):
    account: str
    email: EmailStr
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
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True

# --- Role Schemas ---
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Role(RoleBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True

# --- WebSetting Schemas ---
class WebSettingBase(BaseModel):
    key: str
    name: str
    description: Optional[str] = None
    value: str
    status: str

class WebSettingCreate(WebSettingBase):
    pass

class WebSettingUpdate(BaseModel):
    status: Optional[str] = None

class WebSetting(WebSettingBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True

# --- Library Schemas ---
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
    status: str

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
    status: Optional[str] = None

class Library(LibraryBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True