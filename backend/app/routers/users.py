from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User as UserModel
from schemas import UserCreate, User, UserUpdate
from database import get_db

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Create User
@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(UserModel.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(UserModel).filter(UserModel.email == user.email.lower()).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = UserModel(
        username=user.username,
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

# Get User List (with Pagination)
@router.get("/", response_model=list[User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(UserModel).offset(skip).limit(limit).all()

# Get Single User
@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update User
@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.username is not None:
        db_user.username = user.username
    if user.email is not None:
        db_user.email = user.email.lower()
    if user.real_name is not None:
        db_user.real_name = user.real_name
    if user.password:
        db_user.password = hash_password(user.password)

    db.commit()
    db.refresh(db_user)
    return db_user

# Delete User
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
