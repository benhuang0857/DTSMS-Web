from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from models import UploadedFile as FileModel  # 對應的 UploadedFile 模型
from schemas import UploadedFileCreate, UploadedFileUpdate, UploadedFile  # Schemas 對應 CRUD
from database import get_db
from routers.auth import get_current_user

router = APIRouter()

@router.post("/upload", response_model=UploadedFile)
async def upload_file(
    uploaded_file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    處理檔案上傳，並自動抓取文件信息
    """
    # 取得檔案名稱與類型
    file_name = uploaded_file.filename
    file_type = uploaded_file.content_type

    # 計算檔案大小
    content = await uploaded_file.read()
    file_size = len(content)
    
    # 檢查檔案是否已存在
    if db.query(FileModel).filter(FileModel.name == file_name, FileModel.user_id == current_user.id).first():
        raise HTTPException(status_code=400, detail="相同名稱的檔案已存在")
    
    # 儲存檔案記錄到數據庫
    db_file = FileModel(
        user_id=current_user.id,
        name=file_name,
        ftype=file_type,
        fsize=file_size,
        status="uploaded"
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    # 可選：將文件存儲到伺服器的指定目錄
    with open(f"uploads/{file_name}", "wb") as f:
        f.write(content)

    return db_file

# 獲取檔案列表（支持分頁）
@router.get("/", response_model=List[UploadedFile])
def get_files(skip: int = 0, limit: int = 10, 
              db: Session = Depends(get_db), 
              current_user: dict = Depends(get_current_user)):
    """查詢所有檔案（分頁）"""
    return db.query(FileModel).filter(FileModel.user_id == current_user.id).offset(skip).limit(limit).all()

# 根據 ID 獲取單個檔案
@router.get("/{file_id}", response_model=UploadedFile)
def get_file(file_id: int, 
             db: Session = Depends(get_db),
             current_user: dict = Depends(get_current_user)):
    """根據 ID 查詢檔案"""
    db_file = db.query(FileModel).filter(FileModel.id == file_id, FileModel.user_id == current_user.id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="檔案未找到")
    return db_file

# 更新檔案
@router.put("/{file_id}", response_model=UploadedFile)
def update_file(file_id: int, 
                file: UploadedFileUpdate, 
                db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    """更新檔案資訊"""
    db_file = db.query(FileModel).filter(FileModel.id == file_id, FileModel.user_id == current_user.id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="檔案未找到")

    for key, value in file.dict(exclude_unset=True).items():
        setattr(db_file, key, value)

    db.commit()
    db.refresh(db_file)
    return db_file

# 刪除檔案
@router.delete("/{file_id}", status_code=204)
def delete_file(file_id: int, 
                db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    """刪除檔案"""
    db_file = db.query(FileModel).filter(FileModel.id == file_id, FileModel.user_id == current_user.id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="檔案未找到")
    
    db.delete(db_file)
    db.commit()
    return {"message": "檔案已成功刪除"}
