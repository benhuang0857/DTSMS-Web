from fastapi import Form, APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List, Optional
from models import UploadedFile as FileModel
from schemas import UploadedFileCreate, UploadedFileUpdate, UploadedFile
from database import get_db
from routers.auth import get_current_user
from enums import TrackingStatus

router = APIRouter()

@router.post("/", response_model=UploadedFile)
async def upload_file(
    ticket_id: int = Form(...),
    unzip_password: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    uploaded_file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        file_name = uploaded_file.filename
        file_type = uploaded_file.content_type
        content = await uploaded_file.read()
        file_size = len(content)

        if db.query(FileModel).filter(FileModel.name == file_name, FileModel.user_id == current_user.id).first():
            raise HTTPException(status_code=400, detail="相同名稱的檔案已存在")

        db_file = FileModel(
            user_id=current_user.id,
            ticket_id=ticket_id,
            name=file_name,
            ftype=file_type,
            fsize=file_size,
            unzip_password=unzip_password,
            description=description,
            status="pending"
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        with open(f"uploads/{file_name}", "wb") as f:
            f.write(content)

        return db_file

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

@router.get("/", response_model=List[UploadedFile])
def get_files(skip: int = 0, limit: int = 10, 
              db: Session = Depends(get_db), 
              current_user: dict = Depends(get_current_user)):
    try:
        return db.query(FileModel).filter(FileModel.user_id == current_user.id).offset(skip).limit(limit).all()
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

@router.get("/{file_id}", response_model=UploadedFile)
def get_file(file_id: int, 
             db: Session = Depends(get_db),
             current_user: dict = Depends(get_current_user)):
    try:
        db_file = db.query(FileModel).filter(FileModel.id == file_id, FileModel.user_id == current_user.id).first()
        if not db_file:
            raise HTTPException(status_code=404, detail="檔案未找到")
        return db_file
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

@router.put("/{file_id}", response_model=UploadedFile)
def update_file(file_id: int, 
                file: UploadedFileUpdate, 
                db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    try:
        db_file = db.query(FileModel).filter(FileModel.id == file_id, FileModel.user_id == current_user.id).first()
        if not db_file:
            raise HTTPException(status_code=404, detail="檔案未找到")

        for key, value in file.dict(exclude_unset=True).items():
            setattr(db_file, key, value)

        db.commit()
        db.refresh(db_file)
        return db_file
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

@router.delete("/{file_id}", status_code=204)
def delete_file(file_id: int, 
                db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    try:
        db_file = db.query(FileModel).filter(FileModel.id == file_id, FileModel.user_id == current_user.id).first()
        if not db_file:
            raise HTTPException(status_code=404, detail="檔案未找到")

        db.delete(db_file)
        db.commit()
        return {"message": "檔案已成功刪除"}
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
