from fastapi import Form, APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Optional, List
import os
import zipfile
from models import UploadedFile as FileModel
from schemas import UploadedFile
from database import get_db
from routers.auth import get_current_user
from schemas import UploadedFileUpdate

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
        original_name = uploaded_file.filename
        file_type = uploaded_file.content_type

        # 檢查重複檔名
        if db.query(FileModel).filter(FileModel.name == original_name, FileModel.user_id == current_user.id).first():
            raise HTTPException(status_code=400, detail="相同名稱的檔案已存在")

        # 暫存原始檔
        temp_path = os.path.join(UPLOAD_DIR, f"tmp_{original_name}")
        with open(temp_path, "wb") as f:
            while chunk := await uploaded_file.read(1024 * 1024):  # 1MB chunk
                f.write(chunk)

        # zip 路徑
        zip_name = f"{os.path.splitext(original_name)[0]}.zip"
        zip_path = os.path.join(UPLOAD_DIR, zip_name)

        # 壓縮檔案 + 寫 meta.txt
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(temp_path, arcname=original_name)
            meta_content = f"ticket_code={ticket_id}\nunzip_password={unzip_password or ''}\n"
            zipf.writestr('meta.txt', meta_content)

        # 刪掉原始檔
        os.remove(temp_path)

        # 取得檔案大小
        file_size = os.path.getsize(zip_path)

        # 存 DB
        db_file = FileModel(
            user_id=current_user.id,
            ticket_id=ticket_id,
            name=zip_name,
            ftype="application/zip",
            fsize=file_size,
            unzip_password=unzip_password,
            description=description,
            status="pending"
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

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
