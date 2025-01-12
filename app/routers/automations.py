from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Automation as AutomationModel
from schemas import AutomationCreate, AutomationUpdate, Automation
from database import get_db

router = APIRouter()

# Create a new automation
@router.post("/", response_model=Automation)
def create_automation(automation: AutomationCreate, db: Session = Depends(get_db)):
    db_automation = AutomationModel(**automation.dict())
    db.add(db_automation)
    db.commit()
    db.refresh(db_automation)
    return db_automation

# Get all automations (with optional pagination)
@router.get("/", response_model=List[Automation])
def get_automations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(AutomationModel).offset(skip).limit(limit).all()

# Get a specific automation by ID
@router.get("/{automation_id}", response_model=Automation)
def get_automation(automation_id: int, db: Session = Depends(get_db)):
    automation = db.query(AutomationModel).filter(AutomationModel.id == automation_id).first()
    if not automation:
        raise HTTPException(status_code=404, detail="Automation not found")
    return automation

# Update a specific automation by ID
@router.put("/{automation_id}", response_model=Automation)
def update_automation(automation_id: int, automation: AutomationUpdate, db: Session = Depends(get_db)):
    db_automation = db.query(AutomationModel).filter(AutomationModel.id == automation_id).first()
    if not db_automation:
        raise HTTPException(status_code=404, detail="Automation not found")

    for key, value in automation.dict(exclude_unset=True).items():
        setattr(db_automation, key, value)

    db.commit()
    db.refresh(db_automation)
    return db_automation

# Delete a specific automation by ID
@router.delete("/{automation_id}")
def delete_automation(automation_id: int, db: Session = Depends(get_db)):
    db_automation = db.query(AutomationModel).filter(AutomationModel.id == automation_id).first()
    if not db_automation:
        raise HTTPException(status_code=404, detail="Automation not found")

    db.delete(db_automation)
    db.commit()
    return {"message": "Automation deleted successfully"}
