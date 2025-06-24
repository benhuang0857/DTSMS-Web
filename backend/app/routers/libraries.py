from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Library as LibraryModel  # 確保 Library 模型與數據庫一致
from schemas import LibraryCreate, LibraryUpdate, Library  # Schemas 用於請求/響應驗證
from database import get_db

router = APIRouter()

@router.post("/", response_model=Library)
def create_library(library: LibraryCreate, db: Session = Depends(get_db)):
    db_library = LibraryModel(**library.dict())
    db.add(db_library)
    db.commit()
    db.refresh(db_library)
    return db_library
    
@router.get("/", response_model=list[Library])
def get_libraries(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(LibraryModel).offset(skip).limit(limit).all()