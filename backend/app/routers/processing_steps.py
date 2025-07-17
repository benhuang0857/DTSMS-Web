from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import func
from typing import Optional, List
from models import ProcessingStep as ProcessingStepModel
from models import Autoflow as AutoflowModel
from models import FileTracking as FileTrackingModel
from schemas.processing_step import ProcessingStep, ProcessingStepWithRelations, ProcessingStepCreate, ProcessingStepUpdate
from database import get_db
from routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProcessingStepWithRelations])
def get_processing_steps(skip: int = 0, limit: int = 10, 
                        autoflow_id: Optional[int] = None,
                        db: Session = Depends(get_db), 
                        current_user: dict = Depends(get_current_user)):
    """
    獲取處理步驟列表（包含關聯資料）
    可選擇性過濾特定 autoflow 的步驟
    """
    try:
        # 基本查詢
        query = db.query(ProcessingStepModel)
        
        # 如果指定了 autoflow_id，則過濾
        if autoflow_id:
            query = query.filter(ProcessingStepModel.autoflow_id == autoflow_id)
        
        processing_steps = query.offset(skip).limit(limit).all()
        
        # 轉換為 ProcessingStepWithRelations 格式
        step_list = []
        for step in processing_steps:
            # 取得 autoflow 名稱
            autoflow_name = None
            if step.autoflow_id:
                autoflow = db.query(AutoflowModel).filter(
                    AutoflowModel.id == step.autoflow_id
                ).first()
                if autoflow:
                    autoflow_name = autoflow.name
            
            # 計算 file_trackings 數量
            file_trackings_count = db.query(FileTrackingModel).filter(
                FileTrackingModel.step_id == step.id
            ).count()
            
            step_list.append(
                ProcessingStepWithRelations(
                    id=step.id,
                    autoflow_id=step.autoflow_id,
                    name=step.name,
                    description=step.description,
                    created_time=step.created_time,
                    updated_time=step.updated_time,
                    autoflow_name=autoflow_name,
                    file_trackings_count=file_trackings_count
                )
            )
        
        return step_list
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

@router.get("/{step_id}", response_model=ProcessingStepWithRelations)
def get_processing_step(step_id: int, 
                       db: Session = Depends(get_db),
                       current_user: dict = Depends(get_current_user)):
    """
    根據 ID 獲取特定的處理步驟
    """
    try:
        # 查詢處理步驟
        step = db.query(ProcessingStepModel).filter(
            ProcessingStepModel.id == step_id
        ).first()
        
        if not step:
            raise HTTPException(status_code=404, detail="處理步驟未找到")
        
        # 取得 autoflow 名稱
        autoflow_name = None
        if step.autoflow_id:
            autoflow = db.query(AutoflowModel).filter(
                AutoflowModel.id == step.autoflow_id
            ).first()
            if autoflow:
                autoflow_name = autoflow.name
        
        # 計算 file_trackings 數量
        file_trackings_count = db.query(FileTrackingModel).filter(
            FileTrackingModel.step_id == step.id
        ).count()
        
        return ProcessingStepWithRelations(
            id=step.id,
            autoflow_id=step.autoflow_id,
            name=step.name,
            description=step.description,
            created_time=step.created_time,
            updated_time=step.updated_time,
            autoflow_name=autoflow_name,
            file_trackings_count=file_trackings_count
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

@router.get("/autoflow/{autoflow_id}", response_model=List[ProcessingStepWithRelations])
def get_processing_steps_by_autoflow(autoflow_id: int,
                                    db: Session = Depends(get_db),
                                    current_user: dict = Depends(get_current_user)):
    """
    根據 autoflow_id 獲取該自動化流程的所有處理步驟
    """
    try:
        # 驗證 autoflow 是否存在
        autoflow = db.query(AutoflowModel).filter(
            AutoflowModel.id == autoflow_id
        ).first()
        
        if not autoflow:
            raise HTTPException(status_code=404, detail="自動化流程未找到")
        
        # 查詢處理步驟
        processing_steps = db.query(ProcessingStepModel).filter(
            ProcessingStepModel.autoflow_id == autoflow_id
        ).all()
        
        # 轉換為 ProcessingStepWithRelations 格式
        step_list = []
        for step in processing_steps:
            # 計算 file_trackings 數量
            file_trackings_count = db.query(FileTrackingModel).filter(
                FileTrackingModel.step_id == step.id
            ).count()
            
            step_list.append(
                ProcessingStepWithRelations(
                    id=step.id,
                    autoflow_id=step.autoflow_id,
                    name=step.name,
                    description=step.description,
                    created_time=step.created_time,
                    updated_time=step.updated_time,
                    autoflow_name=autoflow.name,
                    file_trackings_count=file_trackings_count
                )
            )
        
        return step_list
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

@router.post("/", response_model=ProcessingStep)
def create_processing_step(step: ProcessingStepCreate, 
                          db: Session = Depends(get_db),
                          current_user: dict = Depends(get_current_user)):
    """
    創建新的處理步驟
    """
    try:
        # 如果有 autoflow_id，驗證 autoflow 是否存在
        if step.autoflow_id:
            autoflow = db.query(AutoflowModel).filter(
                AutoflowModel.id == step.autoflow_id
            ).first()
            
            if not autoflow:
                raise HTTPException(status_code=404, detail="自動化流程未找到")
        
        # 創建處理步驟
        db_step = ProcessingStepModel(
            autoflow_id=step.autoflow_id,
            name=step.name,
            description=step.description
        )
        
        db.add(db_step)
        db.commit()
        db.refresh(db_step)
        
        return db_step
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

@router.put("/{step_id}", response_model=ProcessingStep)
def update_processing_step(step_id: int, 
                          step: ProcessingStepUpdate,
                          db: Session = Depends(get_db),
                          current_user: dict = Depends(get_current_user)):
    """
    更新處理步驟
    """
    try:
        # 查詢處理步驟
        db_step = db.query(ProcessingStepModel).filter(
            ProcessingStepModel.id == step_id
        ).first()
        
        if not db_step:
            raise HTTPException(status_code=404, detail="處理步驟未找到")
        
        # 如果有 autoflow_id，驗證 autoflow 是否存在
        if step.autoflow_id:
            autoflow = db.query(AutoflowModel).filter(
                AutoflowModel.id == step.autoflow_id
            ).first()
            
            if not autoflow:
                raise HTTPException(status_code=404, detail="自動化流程未找到")
        
        # 更新欄位
        update_data = step.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_step, key, value)
        
        db.commit()
        db.refresh(db_step)
        
        return db_step
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

@router.delete("/{step_id}", status_code=204)
def delete_processing_step(step_id: int,
                          db: Session = Depends(get_db),
                          current_user: dict = Depends(get_current_user)):
    """
    刪除處理步驟（會自動刪除相關的 file_trackings）
    """
    try:
        # 查詢處理步驟
        db_step = db.query(ProcessingStepModel).filter(
            ProcessingStepModel.id == step_id
        ).first()
        
        if not db_step:
            raise HTTPException(status_code=404, detail="處理步驟未找到")
        
        # 先刪除相關的 file_trackings
        db.query(FileTrackingModel).filter(
            FileTrackingModel.step_id == step_id
        ).delete()
        
        # 刪除處理步驟
        db.delete(db_step)
        db.commit()
        
        return {"message": "處理步驟已成功刪除"}
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