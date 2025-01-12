from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Log as LogModel  # Assuming the Log model matches the schema
from schemas import LogCreate, LogUpdate, Log  # Ensure these schemas align with the schema
from database import get_db

router = APIRouter()

# Create a new log
@router.post("/", response_model=Log)
def create_log(log: LogCreate, db: Session = Depends(get_db)):
    """Add a new log entry"""
    db_log = LogModel(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# Get all logs (with pagination)
@router.get("/", response_model=list[Log])
def get_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Retrieve all logs (paginated)"""
    return db.query(LogModel).offset(skip).limit(limit).all()

# Get a specific log by ID
@router.get("/{log_id}", response_model=Log)
def get_log(log_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific log entry by ID"""
    db_log = db.query(LogModel).filter(LogModel.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log

# Update a specific log by ID
@router.put("/{log_id}", response_model=Log)
def update_log(log_id: int, log: LogUpdate, db: Session = Depends(get_db)):
    """Update a specific log entry by ID"""
    db_log = db.query(LogModel).filter(LogModel.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")

    # Update only provided fields
    for key, value in log.dict(exclude_unset=True).items():
        setattr(db_log, key, value)

    db.commit()
    db.refresh(db_log)
    return db_log

# Delete a specific log by ID
@router.delete("/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    """Delete a specific log entry by ID"""
    db_log = db.query(LogModel).filter(LogModel.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")

    db.delete(db_log)
    db.commit()
    return {"message": "Log deleted successfully"}
