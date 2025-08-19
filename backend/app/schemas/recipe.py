from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enums import BasicStatus

class RecipeStepBase(BaseModel):
    number: int
    action: str
    parameters: Optional[Dict[str, Any]] = None
    status: BasicStatus = BasicStatus.active

class RecipeStepCreate(RecipeStepBase):
    pass

class RecipeStepUpdate(BaseModel):
    number: Optional[int] = None
    action: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    status: Optional[BasicStatus] = None

class RecipeStep(RecipeStepBase):
    id: int
    recipe_id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True

class RecipeBase(BaseModel):
    library_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    status: BasicStatus
    allow_parallel_autoflows: bool = False

class RecipeCreate(RecipeBase):
    recipe_steps: Optional[List[RecipeStepCreate]] = []

class RecipeUpdate(BaseModel):
    library_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BasicStatus] = None
    allow_parallel_autoflows: Optional[bool] = None
    recipe_steps: Optional[List[RecipeStepCreate]] = None

class Recipe(RecipeBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True

class RecipeWithRelations(BaseModel):
    id: int
    library_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    status: BasicStatus
    allow_parallel_autoflows: bool = False
    created_time: datetime
    updated_time: datetime
    
    # 關聯的資料
    library_name: Optional[str] = None
    recipe_steps_count: Optional[int] = None
    autoflows_count: Optional[int] = None

    class Config:
        from_attributes = True

class RecipeWithSteps(RecipeWithRelations):
    recipe_steps: List[RecipeStep] = []

    class Config:
        from_attributes = True

class ProcessingStepInfo(BaseModel):
    id: int
    autoflow_id: Optional[int] = None
    library_action_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    execution_order: int = 1
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True

class AutoflowInfo(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: BasicStatus
    allow_parallel_steps: bool = False
    execution_order: int = 1
    created_time: datetime
    updated_time: datetime
    processing_steps: List[ProcessingStepInfo] = []

    class Config:
        from_attributes = True

class RecipeWithFull(RecipeWithSteps):
    autoflows: List[AutoflowInfo] = []

    class Config:
        from_attributes = True