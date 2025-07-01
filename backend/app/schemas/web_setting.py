from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
