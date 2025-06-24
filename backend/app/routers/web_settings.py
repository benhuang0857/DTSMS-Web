from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import WebSetting as WebSettingModel  # 確保 WebSetting 模型與數據庫一致
from schemas import WebSettingCreate, WebSetting, WebSettingUpdate
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[WebSetting])
def get_web_settings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """查詢所有網站設定（分頁）"""
    return db.query(WebSettingModel).offset(skip).limit(limit).all()

@router.put("/{web_setting_id}", response_model=WebSetting)
def update_web_setting(web_setting_id: int, web_setting: WebSettingUpdate, db: Session = Depends(get_db)):
    """根據 ID 更新網站設定"""
    db_web_setting = db.query(WebSettingModel).filter(WebSettingModel.id == web_setting_id).first()
    if not db_web_setting:
        raise HTTPException(status_code=404, detail="網站設定未找到")

    for key, value in web_setting.dict(exclude_unset=True).items():
        setattr(db_web_setting, key, value)

    db.commit()
    db.refresh(db_web_setting)
    return db_web_setting