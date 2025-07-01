from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Role as RoleModel  # 確保 Role 模型與數據庫一致
from schemas import RoleCreate, RoleUpdate, Role  # Schemas 用於請求/響應驗證
from database import get_db
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

# 創建角色
@router.post("/", response_model=Role)
def create_role(
    role: RoleCreate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
    ):
    """新增角色"""
    existing_role = db.query(RoleModel).filter(RoleModel.name == role.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="角色名稱已存在")

    db_role = RoleModel(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# 獲取所有角色（帶分頁功能）
@router.get("/", response_model=list[Role])
def get_roles(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
    ):
    """查詢所有角色（分頁）"""
    return db.query(RoleModel).offset(skip).limit(limit).all()

# 根據 ID 獲取特定角色
@router.get("/{role_id}", response_model=Role)
def get_role(
    role_id: int, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
    ):
    """根據 ID 獲取角色"""
    db_role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="角色未找到")
    return db_role

# 根據 ID 更新角色
@router.put("/{role_id}", response_model=Role)
def update_role(
    role_id: int, 
    role: RoleUpdate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
    ):
    """根據 ID 更新角色"""
    db_role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="角色未找到")

    for key, value in role.dict(exclude_unset=True).items():
        setattr(db_role, key, value)

    db.commit()
    db.refresh(db_role)
    return db_role

# 根據 ID 刪除角色
@router.delete("/{role_id}")
def delete_role(
    role_id: int, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
    ):
    """根據 ID 刪除角色"""
    db_role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="角色未找到")

    db.delete(db_role)
    db.commit()
    return {"message": "角色已成功刪除"}
