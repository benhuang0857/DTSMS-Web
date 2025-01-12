from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import UserCreate, User, UserUpdate
from database import get_db

router = APIRouter()

# 创建用户
@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = UserModel(
        username=user.username,
        email=user.email,
        real_name=user.real_name,
        password=user.password,  # 密码需要加密
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 获取用户列表
@router.get("/", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()

# 获取单个用户
@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 更新用户
@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.username = user.username
    db_user.email = user.email
    db_user.real_name = user.real_name
    if user.password:
        db_user.password = user.password  # 密码更新需要加密
    db.commit()
    db.refresh(db_user)
    return db_user

# 删除用户
@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return db_user
