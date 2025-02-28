from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from models import FileUpload as FileUploadModel
from schemas import FileUploadCreate, FileUploadUpdate, FileUpload
from database import get_db
import os
from pathlib import Path
import uuid
import time
import shutil

router = APIRouter()

# 定義文件儲存目錄
UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

# 可接受的文件類型
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def secure_filename(filename: str) -> str:
    """生成安全的文件名，避免覆蓋"""
    base, ext = os.path.splitext(filename)
    timestamp = int(time.time())
    return f"{base}_{timestamp}{ext}"

def generate_tracking_num(db: Session) -> str:
    """生成唯一的 tracking_num"""
    while True:
        # 使用 UUID 生成唯一字符串（可根據需求調整格式）
        tracking_num = f"TRACK-{uuid.uuid4().hex[:8].upper()}"
        # 檢查是否已存在
        if not db.query(FileUploadModel).filter(FileUploadModel.tracking_num == tracking_num).first():
            return tracking_num

@router.post("/", response_model=FileUpload)
async def create_file_upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Add a new file upload record with auto-generated tracking_num"""
    # 生成唯一的 tracking_num
    tracking_num = generate_tracking_num(db)

    # 使用 secure_filename 生成安全的文件名
    safe_filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    # 儲存文件到本地
    file_content = await file.read()
    with open(file_path, "wb") as f:
        f.write(file_content)

    # 創建數據庫記錄
    db_file_upload = FileUploadModel(
        tracking_num=tracking_num,
        filename=safe_filename,  # 使用安全的文件名
        size=len(file_content),
        file_path=file_path,
        user_id=None,
        token=None,
        status="process"
    )
    db.add(db_file_upload)
    db.commit()
    db.refresh(db_file_upload)
    return db_file_upload

@router.get("/", response_model=list[FileUpload])
def get_file_uploads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Retrieve all file upload records (paginated)"""
    return db.query(FileUploadModel).offset(skip).limit(limit).all()

@router.get("/{file_upload_id}", response_model=FileUpload)
def get_file_upload(file_upload_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific file upload record by ID"""
    db_file_upload = db.query(FileUploadModel).filter(FileUploadModel.id == file_upload_id).first()
    if not db_file_upload:
        raise HTTPException(status_code=404, detail="File upload not found")
    return db_file_upload

@router.put("/{file_upload_id}", response_model=FileUpload)
def update_file_upload(file_upload_id: int, file_upload: FileUploadUpdate, db: Session = Depends(get_db)):
    """Update a specific file upload record by ID"""
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
    """Delete a specific file upload record by ID and remove the file"""
    db_file_upload = db.query(FileUploadModel).filter(FileUploadModel.id == file_upload_id).first()
    if not db_file_upload:
        raise HTTPException(status_code=404, detail="File upload not found")

    # 刪除本地文件
    if os.path.exists(db_file_upload.file_path):
        try:
            os.remove(db_file_upload.file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

    db.delete(db_file_upload)
    db.commit()
    return {"message": "File upload deleted successfully"}