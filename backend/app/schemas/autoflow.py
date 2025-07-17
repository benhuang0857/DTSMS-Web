from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enums import BasicStatus
from .processing_step import ProcessingStepCreate

class AutoflowBase(BaseModel):
    recipe_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    status: BasicStatus

class AutoflowCreate(AutoflowBase):
    processing_steps: Optional[List[ProcessingStepCreate]] = []

class AutoflowUpdate(BaseModel):
    recipe_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BasicStatus] = None
    processing_steps: Optional[List[ProcessingStepCreate]] = None

class Autoflow(AutoflowBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True

class AutoflowWithRelations(BaseModel):
    id: int
    recipe_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    status: BasicStatus
    created_time: datetime
    updated_time: datetime
    
    # 關聯的資料
    recipe_name: Optional[str] = None
    recipe_description: Optional[str] = None
    processing_steps_count: Optional[int] = None

    class Config:
        from_attributes = True

class AutoflowWithSteps(AutoflowWithRelations):
    processing_steps: List[dict] = []

    class Config:
        from_attributes = True

class RecipeInfo(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: BasicStatus
    created_time: datetime
    updated_time: datetime
    recipe_steps: List[dict] = []

    class Config:
        from_attributes = True

class AutoflowWithFull(AutoflowWithSteps):
    recipe: Optional[RecipeInfo] = None

    class Config:
        from_attributes = True