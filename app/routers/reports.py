from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Report as ReportModel  # Assuming the Report model matches the schema
from schemas import ReportCreate, ReportUpdate, Report  # Ensure these schemas align with the schema
from database import get_db

router = APIRouter()

# Create a new report
@router.post("/", response_model=Report)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    """Add a new report record"""
    db_report = ReportModel(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

# Get all reports (with pagination)
@router.get("/", response_model=list[Report])
def get_reports(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Retrieve all report records (paginated)"""
    return db.query(ReportModel).offset(skip).limit(limit).all()

# Get a specific report by ID
@router.get("/{report_id}", response_model=Report)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific report by ID"""
    db_report = db.query(ReportModel).filter(ReportModel.id == report_id).first()
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

# Update a specific report by ID
@router.put("/{report_id}", response_model=Report)
def update_report(report_id: int, report: ReportUpdate, db: Session = Depends(get_db)):
    """Update a specific report record by ID"""
    db_report = db.query(ReportModel).filter(ReportModel.id == report_id).first()
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Update only provided fields
    for key, value in report.dict(exclude_unset=True).items():
        setattr(db_report, key, value)

    db.commit()
    db.refresh(db_report)
    return db_report

# Delete a specific report by ID
@router.delete("/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    """Delete a specific report record by ID"""
    db_report = db.query(ReportModel).filter(ReportModel.id == report_id).first()
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(db_report)
    db.commit()
    return {"message": "Report deleted successfully"}
