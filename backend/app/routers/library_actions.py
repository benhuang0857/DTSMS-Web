from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import LibraryAction as LibraryActionModel, Library as LibraryModel
from schemas import LibraryActionCreate, LibraryActionUpdate, LibraryAction
from database import get_db
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

@router.post("/", response_model=LibraryAction)
def create_library_action(
    action: LibraryActionCreate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new library action"""
    # Check if library exists
    library = db.query(LibraryModel).filter(LibraryModel.id == action.library_id).first()
    if not library:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Library not found"
        )
    
    # Check if action name already exists for this library
    existing_action = db.query(LibraryActionModel).filter(
        LibraryActionModel.library_id == action.library_id,
        LibraryActionModel.name == action.name
    ).first()
    if existing_action:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Action name already exists for this library"
        )
    
    db_action = LibraryActionModel(**action.dict())
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action

@router.get("/", response_model=List[LibraryAction])
def get_library_actions(
    skip: int = 0, 
    limit: int = 100, 
    library_id: int = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all library actions, optionally filtered by library_id"""
    query = db.query(LibraryActionModel)
    if library_id:
        query = query.filter(LibraryActionModel.library_id == library_id)
    return query.offset(skip).limit(limit).all()

@router.get("/{action_id}", response_model=LibraryAction)
def get_library_action(
    action_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific library action by ID"""
    action = db.query(LibraryActionModel).filter(LibraryActionModel.id == action_id).first()
    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Library action not found"
        )
    return action

@router.put("/{action_id}", response_model=LibraryAction)
def update_library_action(
    action_id: int,
    action_update: LibraryActionUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a library action"""
    db_action = db.query(LibraryActionModel).filter(LibraryActionModel.id == action_id).first()
    if not db_action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Library action not found"
        )
    
    # Check for duplicate name if name is being updated
    if action_update.name and action_update.name != db_action.name:
        existing_action = db.query(LibraryActionModel).filter(
            LibraryActionModel.library_id == db_action.library_id,
            LibraryActionModel.name == action_update.name,
            LibraryActionModel.id != action_id
        ).first()
        if existing_action:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Action name already exists for this library"
            )
    
    update_data = action_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_action, field, value)
    
    db.commit()
    db.refresh(db_action)
    return db_action

@router.delete("/{action_id}")
def delete_library_action(
    action_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a library action"""
    db_action = db.query(LibraryActionModel).filter(LibraryActionModel.id == action_id).first()
    if not db_action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Library action not found"
        )
    
    db.delete(db_action)
    db.commit()
    return {"message": "Library action deleted successfully"}

@router.get("/library/{library_id}", response_model=List[LibraryAction])
def get_actions_by_library(
    library_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all actions for a specific library"""
    # Check if library exists
    library = db.query(LibraryModel).filter(LibraryModel.id == library_id).first()
    if not library:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Library not found"
        )
    
    return db.query(LibraryActionModel).filter(LibraryActionModel.library_id == library_id).all()