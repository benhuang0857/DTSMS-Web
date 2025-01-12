from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Action as ActionModel
from schemas import ActionCreate, ActionUpdate, Action
from database import get_db

router = APIRouter()

# Create a new action
@router.post("/", response_model=Action)
def create_action(action: ActionCreate, db: Session = Depends(get_db)):
    db_action = ActionModel(**action.dict())
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action

# Get all actions (with optional pagination)
@router.get("/", response_model=List[Action])
def get_actions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ActionModel).offset(skip).limit(limit).all()

# Get a specific action by ID
@router.get("/{action_id}", response_model=Action)
def get_action(action_id: int, db: Session = Depends(get_db)):
    action = db.query(ActionModel).filter(ActionModel.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return action

# Update a specific action by ID
@router.put("/{action_id}", response_model=Action)
def update_action(action_id: int, action: ActionUpdate, db: Session = Depends(get_db)):
    db_action = db.query(ActionModel).filter(ActionModel.id == action_id).first()
    if not db_action:
        raise HTTPException(status_code=404, detail="Action not found")

    for key, value in action.dict(exclude_unset=True).items():
        setattr(db_action, key, value)

    db.commit()
    db.refresh(db_action)
    return db_action

# Delete a specific action by ID
@router.delete("/{action_id}")
def delete_action(action_id: int, db: Session = Depends(get_db)):
    db_action = db.query(ActionModel).filter(ActionModel.id == action_id).first()
    if not db_action:
        raise HTTPException(status_code=404, detail="Action not found")

    db.delete(db_action)
    db.commit()
    return {"message": "Action deleted successfully"}
