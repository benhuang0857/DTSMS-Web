from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProcessingStepBase(BaseModel):
    autoflow_id: Optional[int] = None
    library_action_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    execution_order: int = 1

class ProcessingStepCreate(BaseModel):
    library_action_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    execution_order: int = 1

class ProcessingStepUpdate(BaseModel):
    autoflow_id: Optional[int] = None
    library_action_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    execution_order: Optional[int] = None

class ProcessingStep(ProcessingStepBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True

class ProcessingStepWithRelations(BaseModel):
    id: int
    autoflow_id: Optional[int] = None
    library_action_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    execution_order: int = 1
    created_time: datetime
    updated_time: datetime
    
    # 關聯的資料
    autoflow_name: Optional[str] = None
    library_action_name: Optional[str] = None
    file_trackings_count: Optional[int] = None

    class Config:
        from_attributes = True