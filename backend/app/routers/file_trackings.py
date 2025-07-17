from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Optional, List
from models import FileTracking as TrackingModel
from models import UploadedFile as FileModel
from models import ProcessingStep as ProcessingStepModel
from schemas.file_tracking import FileTracking, FileTrackingWithRelations, FileTrackingCreate, FileTrackingUpdate
from database import get_db
from routers.auth import get_current_user
from datetime import datetime
import uuid

router = APIRouter()

@router.get("/", response_model=List[FileTrackingWithRelations])
def get_file_trackings(skip: int = 0, limit: int = 10, 
                      db: Session = Depends(get_db), 
                      current_user: dict = Depends(get_current_user)):
    """
    獲取文件追蹤記錄列表（包含關聯資料）
    """
    try:
        # 使用 JOIN 查詢來獲取關聯資料
        query = db.query(
            TrackingModel.id,
            TrackingModel.tracking_id,
            TrackingModel.uploaded_file_id,
            TrackingModel.step_id,
            TrackingModel.start_time,
            TrackingModel.end_time,
            TrackingModel.result,
            TrackingModel.status,
            TrackingModel.note,
            TrackingModel.created_time,
            TrackingModel.updated_time,
            FileModel.name.label('uploaded_file_name'),
            FileModel.status.label('uploaded_file_status'),
            FileModel.user_id,
            ProcessingStepModel.name.label('step_name'),
            ProcessingStepModel.description.label('step_description')
        ).join(
            FileModel, TrackingModel.uploaded_file_id == FileModel.id
        ).join(
            ProcessingStepModel, TrackingModel.step_id == ProcessingStepModel.id
        ).filter(
            FileModel.user_id == current_user.id
        ).offset(skip).limit(limit)
        
        results = query.all()
        
        # 轉換為 FileTrackingWithRelations 格式
        return [
            FileTrackingWithRelations(
                id=row.id,
                tracking_id=row.tracking_id,
                uploaded_file_id=row.uploaded_file_id,
                step_id=row.step_id,
                start_time=row.start_time,
                end_time=row.end_time,
                result=row.result,
                status=row.status,
                note=row.note,
                created_time=row.created_time,
                updated_time=row.updated_time,
                uploaded_file_name=row.uploaded_file_name,
                uploaded_file_status=row.uploaded_file_status,
                step_name=row.step_name,
                step_description=row.step_description,
                user_id=row.user_id
            ) for row in results
        ]
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

@router.get("/{tracking_id}", response_model=FileTrackingWithRelations)
def get_file_tracking(tracking_id: str, 
                     db: Session = Depends(get_db),
                     current_user: dict = Depends(get_current_user)):
    """
    根據 tracking_id 獲取特定的文件追蹤記錄
    """
    try:
        # 驗證 UUID 格式
        try:
            uuid_obj = uuid.UUID(tracking_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="無效的 tracking_id 格式")
        
        # 查詢追蹤記錄
        query = db.query(
            TrackingModel.id,
            TrackingModel.tracking_id,
            TrackingModel.uploaded_file_id,
            TrackingModel.step_id,
            TrackingModel.start_time,
            TrackingModel.end_time,
            TrackingModel.result,
            TrackingModel.status,
            TrackingModel.note,
            TrackingModel.created_time,
            TrackingModel.updated_time,
            FileModel.name.label('uploaded_file_name'),
            FileModel.status.label('uploaded_file_status'),
            FileModel.user_id,
            ProcessingStepModel.name.label('step_name'),
            ProcessingStepModel.description.label('step_description')
        ).join(
            FileModel, TrackingModel.uploaded_file_id == FileModel.id
        ).join(
            ProcessingStepModel, TrackingModel.step_id == ProcessingStepModel.id
        ).filter(
            TrackingModel.tracking_id == uuid_obj,
            FileModel.user_id == current_user.id
        )
        
        result = query.first()
        
        if not result:
            raise HTTPException(status_code=404, detail="追蹤記錄未找到")
        
        return FileTrackingWithRelations(
            id=result.id,
            tracking_id=result.tracking_id,
            uploaded_file_id=result.uploaded_file_id,
            step_id=result.step_id,
            start_time=result.start_time,
            end_time=result.end_time,
            result=result.result,
            status=result.status,
            note=result.note,
            created_time=result.created_time,
            updated_time=result.updated_time,
            uploaded_file_name=result.uploaded_file_name,
            uploaded_file_status=result.uploaded_file_status,
            step_name=result.step_name,
            step_description=result.step_description,
            user_id=result.user_id
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

@router.get("/file/{uploaded_file_id}", response_model=List[FileTrackingWithRelations])
def get_file_trackings_by_file(uploaded_file_id: int, 
                              db: Session = Depends(get_db),
                              current_user: dict = Depends(get_current_user)):
    """
    根據 uploaded_file_id 獲取該文件的所有追蹤記錄
    """
    try:
        # 查詢追蹤記錄
        query = db.query(
            TrackingModel.id,
            TrackingModel.tracking_id,
            TrackingModel.uploaded_file_id,
            TrackingModel.step_id,
            TrackingModel.start_time,
            TrackingModel.end_time,
            TrackingModel.result,
            TrackingModel.status,
            TrackingModel.note,
            TrackingModel.created_time,
            TrackingModel.updated_time,
            FileModel.name.label('uploaded_file_name'),
            FileModel.status.label('uploaded_file_status'),
            FileModel.user_id,
            ProcessingStepModel.name.label('step_name'),
            ProcessingStepModel.description.label('step_description')
        ).join(
            FileModel, TrackingModel.uploaded_file_id == FileModel.id
        ).join(
            ProcessingStepModel, TrackingModel.step_id == ProcessingStepModel.id
        ).filter(
            TrackingModel.uploaded_file_id == uploaded_file_id,
            FileModel.user_id == current_user.id
        ).order_by(TrackingModel.created_time.desc())
        
        results = query.all()
        
        # 轉換為 FileTrackingWithRelations 格式
        return [
            FileTrackingWithRelations(
                id=row.id,
                tracking_id=row.tracking_id,
                uploaded_file_id=row.uploaded_file_id,
                step_id=row.step_id,
                start_time=row.start_time,
                end_time=row.end_time,
                result=row.result,
                status=row.status,
                note=row.note,
                created_time=row.created_time,
                updated_time=row.updated_time,
                uploaded_file_name=row.uploaded_file_name,
                uploaded_file_status=row.uploaded_file_status,
                step_name=row.step_name,
                step_description=row.step_description,
                user_id=row.user_id
            ) for row in results
        ]
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

@router.post("/", response_model=FileTracking)
def create_file_tracking(tracking: FileTrackingCreate, 
                        db: Session = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    """
    創建新的文件追蹤記錄
    """
    try:
        # 驗證 uploaded_file 是否屬於當前用戶
        uploaded_file = db.query(FileModel).filter(
            FileModel.id == tracking.uploaded_file_id,
            FileModel.user_id == current_user.id
        ).first()
        
        if not uploaded_file:
            raise HTTPException(status_code=404, detail="檔案未找到或無權限")
        
        # 驗證 processing_step 是否存在
        processing_step = db.query(ProcessingStepModel).filter(
            ProcessingStepModel.id == tracking.step_id
        ).first()
        
        if not processing_step:
            raise HTTPException(status_code=404, detail="處理步驟未找到")
        
        # 創建追蹤記錄
        db_tracking = TrackingModel(
            uploaded_file_id=tracking.uploaded_file_id,
            step_id=tracking.step_id,
            start_time=tracking.start_time,
            end_time=tracking.end_time,
            result=tracking.result,
            status=tracking.status,
            note=tracking.note
        )
        
        db.add(db_tracking)
        db.commit()
        db.refresh(db_tracking)
        
        return db_tracking
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

@router.put("/{tracking_id}", response_model=FileTracking)
def update_file_tracking(tracking_id: str, 
                        tracking: FileTrackingUpdate,
                        db: Session = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    """
    更新文件追蹤記錄
    """
    try:
        # 驗證 UUID 格式
        try:
            uuid_obj = uuid.UUID(tracking_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="無效的 tracking_id 格式")
        
        # 查詢追蹤記錄
        db_tracking = db.query(TrackingModel).join(
            FileModel, TrackingModel.uploaded_file_id == FileModel.id
        ).filter(
            TrackingModel.tracking_id == uuid_obj,
            FileModel.user_id == current_user.id
        ).first()
        
        if not db_tracking:
            raise HTTPException(status_code=404, detail="追蹤記錄未找到")
        
        # 更新欄位
        update_data = tracking.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tracking, key, value)
        
        db.commit()
        db.refresh(db_tracking)
        
        return db_tracking
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

@router.delete("/{tracking_id}", status_code=204)
def delete_file_tracking(tracking_id: str,
                        db: Session = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    """
    刪除文件追蹤記錄
    """
    try:
        # 驗證 UUID 格式
        try:
            uuid_obj = uuid.UUID(tracking_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="無效的 tracking_id 格式")
        
        # 查詢追蹤記錄
        db_tracking = db.query(TrackingModel).join(
            FileModel, TrackingModel.uploaded_file_id == FileModel.id
        ).filter(
            TrackingModel.tracking_id == uuid_obj,
            FileModel.user_id == current_user.id
        ).first()
        
        if not db_tracking:
            raise HTTPException(status_code=404, detail="追蹤記錄未找到")
        
        db.delete(db_tracking)
        db.commit()
        
        return {"message": "追蹤記錄已成功刪除"}
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