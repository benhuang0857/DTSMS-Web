from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enums import WebSettingStatus

class WebSettingBase(BaseModel):
    key: str
    name: str
    description: Optional[str] = None
    value: str
    status: WebSettingStatus

class WebSettingCreate(WebSettingBase):
    pass

class WebSettingUpdate(BaseModel):
    status: Optional[WebSettingStatus] = None

class WebSetting(WebSettingBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        orm_mode = True
