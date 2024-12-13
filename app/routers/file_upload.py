from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import FileUpload as FileUploadModel  # Corrected model import
from schemas import FileUploadCreate, FileUploadUpdate, FileUpload  # Corrected schema import
from database import get_db  # Assume get_db is imported from the database module

router = APIRouter()

@router.post("/", response_model=FileUpload)
def create_file_upload(file_upload: FileUploadCreate, db: Session = Depends(get_db)):
    """新增一筆檔案上傳紀錄"""
    db_file_upload = FileUploadModel(**file_upload.dict())  # Corrected model usage
    db.add(db_file_upload)
    db.commit()
    db.refresh(db_file_upload)
    return db_file_upload

@router.get("/", response_model=list[FileUpload])
def get_file_uploads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """取得所有檔案上傳紀錄 (分頁)"""
    return db.query(FileUploadModel).offset(skip).limit(limit).all()

@router.get("/{file_upload_id}", response_model=FileUpload)
def get_file_upload(file_upload_id: int, db: Session = Depends(get_db)):
    """取得特定 ID 的檔案上傳紀錄"""
    db_file_upload = db.query(FileUploadModel).filter(FileUploadModel.id == file_upload_id).first()
    if not db_file_upload:
        raise HTTPException(status_code=404, detail="File upload not found")
    return db_file_upload

@router.put("/{file_upload_id}", response_model=FileUpload)
def update_file_upload(file_upload_id: int, file_upload: FileUploadUpdate, db: Session = Depends(get_db)):
    """更新特定 ID 的檔案上傳紀錄"""
    db_file_upload = db.query(FileUploadModel).filter(FileUploadModel.id == file_upload_id).first()
    if not db_file_upload:
        raise HTTPException(status_code=404, detail="File upload not found")

    for key, value in file_upload.dict(exclude_unset=True).items():
        setattr(db_file_upload, key, value)

    db.commit()
    db.refresh(db_file_upload)
    return db_file_upload

@router.delete("/{file_upload_id}")
def delete_file_upload(file_upload_id: int, db: Session = Depends(get_db)):
    """刪除特定 ID 的檔案上傳紀錄"""
    db_file_upload = db.query(FileUploadModel).filter(FileUploadModel.id == file_upload_id).first()
    if not db_file_upload:
        raise HTTPException(status_code=404, detail="File upload not found")

    db.delete(db_file_upload)
    db.commit()
    return {"message": "File upload deleted successfully"}
