from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext
from models import User as UserModel
from schemas import UserCreate, User, UserUpdate
from database import get_db
from routers.auth import get_current_user

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

# 創建新用戶
@router.post("/", response_model=User)
def create_user(user: UserCreate, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    """新增用戶"""
    if db.query(UserModel).filter(UserModel.account == user.account).first():
        raise HTTPException(status_code=400, detail="用戶名已被註冊")
    if db.query(UserModel).filter(UserModel.email == user.email.lower()).first():
        raise HTTPException(status_code=400, detail="電子郵件已被註冊")

    db_user = UserModel(
        account=user.account,
        email=user.email.lower(),
        avatar=user.avatar,
        real_name=user.real_name,
        organization=user.organization,
        address=user.address,
        mobile=user.mobile,
        password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 獲取用戶列表（支持分頁）
@router.get("/", response_model=list[User])
def get_users(skip: int = 0, limit: int = 10, 
              db: Session = Depends(get_db), 
              current_user: UserModel = Depends(get_current_user)):
    users = db.query(UserModel).options(joinedload(UserModel.role)).offset(skip).limit(limit).all()
    return users

# 獲取單個用戶
@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, 
             db: Session = Depends(get_db),
             current_user: UserModel = Depends(get_current_user)):
    """根據 ID 獲取用戶"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用戶未找到")
    return db_user

# 更新用戶
@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    """更新用戶資料"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用戶未找到")
    
    for key, value in user.dict(exclude_unset=True).items():
        if key == "password" and value:
            value = hash_password(value)
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# 刪除用戶
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    """刪除用戶"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用戶未找到")
    
    db.delete(db_user)
    db.commit()
    return {"message": "用戶已成功刪除"}
