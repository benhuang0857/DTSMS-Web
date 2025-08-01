from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import func
from typing import Optional, List
from models import Autoflow as AutoflowModel
from models import Recipe as RecipeModel
from models import RecipeStep as RecipeStepModel
from models import ProcessingStep as ProcessingStepModel
from schemas.autoflow import Autoflow, AutoflowWithRelations, AutoflowWithSteps, AutoflowWithFull, AutoflowCreate, AutoflowUpdate
from database import get_db
from routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[AutoflowWithFull])
def get_autoflows(skip: int = 0, limit: int = 10, 
                  db: Session = Depends(get_db), 
                  current_user: dict = Depends(get_current_user)):
    """
    獲取自動化流程列表（包含完整的關聯資料：recipe、recipe_steps 和 processing_steps）
    """
    try:
        # 查詢自動化流程
        autoflows = db.query(AutoflowModel).offset(skip).limit(limit).all()
        
        # 轉換為 AutoflowWithFull 格式
        autoflow_list = []
        for autoflow in autoflows:
            # 查詢 processing_steps
            processing_steps = db.query(ProcessingStepModel).filter(
                ProcessingStepModel.autoflow_id == autoflow.id
            ).all()
            
            # 轉換 processing_steps 為字典格式
            processing_steps_data = [
                {
                    "id": step.id,
                    "name": step.name,
                    "description": step.description,
                    "created_time": step.created_time,
                    "updated_time": step.updated_time
                } for step in processing_steps
            ]
            
            # 查詢 recipe 資訊
            recipe_data = None
            recipe_name = None
            recipe_description = None
            
            if autoflow.recipe_id:
                recipe = db.query(RecipeModel).filter(
                    RecipeModel.id == autoflow.recipe_id
                ).first()
                
                if recipe:
                    recipe_name = recipe.name
                    recipe_description = recipe.description
                    
                    # 查詢 recipe_steps
                    recipe_steps = db.query(RecipeStepModel).filter(
                        RecipeStepModel.recipe_id == recipe.id
                    ).order_by(RecipeStepModel.number).all()
                    
                    # 轉換 recipe_steps 為字典格式
                    recipe_steps_data = [
                        {
                            "id": step.id,
                            "recipe_id": step.recipe_id,
                            "number": step.number,
                            "action": step.action,
                            "parameters": step.parameters,
                            "status": step.status,
                            "created_time": step.created_time,
                            "updated_time": step.updated_time
                        } for step in recipe_steps
                    ]
                    
                    recipe_data = {
                        "id": recipe.id,
                        "name": recipe.name,
                        "description": recipe.description,
                        "status": recipe.status,
                        "created_time": recipe.created_time,
                        "updated_time": recipe.updated_time,
                        "recipe_steps": recipe_steps_data
                    }
            
            autoflow_list.append(
                AutoflowWithFull(
                    id=autoflow.id,
                    recipe_id=autoflow.recipe_id,
                    name=autoflow.name,
                    description=autoflow.description,
                    status=autoflow.status,
                    allow_parallel_steps=autoflow.allow_parallel_steps,
                    execution_order=autoflow.execution_order,
                    created_time=autoflow.created_time,
                    updated_time=autoflow.updated_time,
                    recipe_name=recipe_name,
                    recipe_description=recipe_description,
                    processing_steps_count=len(processing_steps_data),
                    processing_steps=processing_steps_data,
                    recipe=recipe_data
                )
            )
        
        return autoflow_list
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.get("/{autoflow_id}", response_model=AutoflowWithSteps)
def get_autoflow(autoflow_id: int, 
                 db: Session = Depends(get_db),
                 current_user: dict = Depends(get_current_user)):
    """
    根據 ID 獲取特定的自動化流程（包含處理步驟）
    """
    try:
        # 查詢自動化流程
        autoflow_result = db.query(AutoflowModel).filter(
            AutoflowModel.id == autoflow_id
        ).first()
        
        if not autoflow_result:
            raise HTTPException(status_code=404, detail="自動化流程未找到")
        
        # 查詢處理步驟
        processing_steps = db.query(ProcessingStepModel).filter(
            ProcessingStepModel.autoflow_id == autoflow_id
        ).all()
        
        # 轉換處理步驟為字典格式
        steps_data = [
            {
                "id": step.id,
                "name": step.name,
                "description": step.description,
                "created_time": step.created_time,
                "updated_time": step.updated_time
            } for step in processing_steps
        ]
        
        return AutoflowWithSteps(
            id=autoflow_result.id,
            recipe_id=autoflow_result.recipe_id,
            name=autoflow_result.name,
            description=autoflow_result.description,
            status=autoflow_result.status,
            allow_parallel_steps=autoflow_result.allow_parallel_steps,
            execution_order=autoflow_result.execution_order,
            created_time=autoflow_result.created_time,
            updated_time=autoflow_result.updated_time,
            recipe_name=None,  # 暫時設為 None
            recipe_description=None,  # 暫時設為 None
            processing_steps_count=len(steps_data),
            processing_steps=steps_data
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.post("/", response_model=Autoflow)
def create_autoflow(autoflow: AutoflowCreate, 
                   db: Session = Depends(get_db),
                   current_user: dict = Depends(get_current_user)):
    """
    創建新的自動化流程
    """
    try:
        # 如果有 recipe_id，驗證 recipe 是否存在
        if autoflow.recipe_id:
            recipe = db.query(RecipeModel).filter(
                RecipeModel.id == autoflow.recipe_id
            ).first()
            
            if not recipe:
                raise HTTPException(status_code=404, detail="Recipe 未找到")
        
        # 創建自動化流程
        db_autoflow = AutoflowModel(
            recipe_id=autoflow.recipe_id,
            name=autoflow.name,
            description=autoflow.description,
            status=autoflow.status,
            allow_parallel_steps=autoflow.allow_parallel_steps,
            execution_order=autoflow.execution_order
        )
        
        db.add(db_autoflow)
        db.flush()  # 先 flush 以取得 autoflow ID
        
        # 創建處理步驟
        if autoflow.processing_steps:
            for step_data in autoflow.processing_steps:
                db_step = ProcessingStepModel(
                    autoflow_id=db_autoflow.id,
                    name=step_data.name,
                    description=step_data.description,
                    execution_order=step_data.execution_order
                )
                db.add(db_step)
        
        db.commit()
        db.refresh(db_autoflow)
        
        return db_autoflow
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫完整性錯誤: {str(e)}"}
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.put("/{autoflow_id}", response_model=Autoflow)
def update_autoflow(autoflow_id: int, 
                   autoflow: AutoflowUpdate,
                   db: Session = Depends(get_db),
                   current_user: dict = Depends(get_current_user)):
    """
    更新自動化流程
    """
    try:
        # 查詢自動化流程
        db_autoflow = db.query(AutoflowModel).filter(
            AutoflowModel.id == autoflow_id
        ).first()
        
        if not db_autoflow:
            raise HTTPException(status_code=404, detail="自動化流程未找到")
        
        # 如果有 recipe_id，驗證 recipe 是否存在
        if autoflow.recipe_id:
            recipe = db.query(RecipeModel).filter(
                RecipeModel.id == autoflow.recipe_id
            ).first()
            
            if not recipe:
                raise HTTPException(status_code=404, detail="Recipe 未找到")
        
        # 更新欄位
        update_data = autoflow.dict(exclude_unset=True)
        processing_steps = update_data.pop('processing_steps', None)
        
        for key, value in update_data.items():
            setattr(db_autoflow, key, value)
        
        # 如果有提供 processing_steps，則更新處理步驟
        if processing_steps is not None:
            # 刪除現有的處理步驟
            db.query(ProcessingStepModel).filter(
                ProcessingStepModel.autoflow_id == autoflow_id
            ).delete()
            
            # 創建新的處理步驟
            for step_data in processing_steps:
                db_step = ProcessingStepModel(
                    autoflow_id=db_autoflow.id,
                    name=step_data.name,
                    description=step_data.description,
                    execution_order=step_data.execution_order
                )
                db.add(db_step)
        
        db.commit()
        db.refresh(db_autoflow)
        
        return db_autoflow
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫完整性錯誤: {str(e)}"}
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.delete("/{autoflow_id}", status_code=204)
def delete_autoflow(autoflow_id: int,
                   db: Session = Depends(get_db),
                   current_user: dict = Depends(get_current_user)):
    """
    刪除自動化流程
    """
    try:
        # 查詢自動化流程
        db_autoflow = db.query(AutoflowModel).filter(
            AutoflowModel.id == autoflow_id
        ).first()
        
        if not db_autoflow:
            raise HTTPException(status_code=404, detail="自動化流程未找到")
        
        # 先刪除相關的處理步驟
        db.query(ProcessingStepModel).filter(
            ProcessingStepModel.autoflow_id == autoflow_id
        ).delete()
        
        # 再刪除自動化流程
        db.delete(db_autoflow)
        db.commit()
        
        return {"message": "自動化流程已成功刪除"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )