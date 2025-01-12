from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import FileUpload as FileUploadModel  # Ensure this model matches the schema
from schemas import FileUploadCreate, FileUploadUpdate, FileUpload  # Ensure these schemas match the schema
from database import get_db  # Dependency to get the database session

router = APIRouter()

# Create a new file upload record
@router.post("/", response_model=FileUpload)
def create_file_upload(file_upload: FileUploadCreate, db: Session = Depends(get_db)):
    """Add a new file upload record"""
    # Check if tracking_num is unique
    existing_file = db.query(FileUploadModel).filter(FileUploadModel.tracking_num == file_upload.tracking_num).first()
    if existing_file:
        raise HTTPException(status_code=400, detail="Tracking number already exists")

    db_file_upload = FileUploadModel(**file_upload.dict())
    db.add(db_file_upload)
    db.commit()
    db.refresh(db_file_upload)
    return db_file_upload

# Get all file upload records (with pagination)
@router.get("/", response_model=list[FileUpload])
def get_file_uploads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Retrieve all file upload records (paginated)"""
    return db.query(FileUploadModel).offset(skip).limit(limit).all()

# Get a specific file upload record by ID
@router.get("/{file_upload_id}", response_model=FileUpload)
def get_file_upload(file_upload_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific file upload record by ID"""
    db_file_upload = db.query(FileUploadModel).filter(FileUploadModel.id == file_upload_id).first()
    if not db_file_upload:
        raise HTTPException(status_code=404, detail="File upload not found")
    return db_file_upload

# Update a specific file upload record by ID
@router.put("/{file_upload_id}", response_model=FileUpload)
def update_file_upload(file_upload_id: int, file_upload: FileUploadUpdate, db: Session = Depends(get_db)):
    """Update a specific file upload record by ID"""
    db_file_upload = db.query(FileUploadModel).filter(FileUploadModel.id == file_upload_id).first()
    if not db_file_upload:
        raise HTTPException(status_code=404, detail="File upload not found")

    # Update only provided fields
    for key, value in file_upload.dict(exclude_unset=True).items():
        setattr(db_file_upload, key, value)

    db.commit()
    db.refresh(db_file_upload)
    return db_file_upload

# Delete a specific file upload record by ID
@router.delete("/{file_upload_id}")
def delete_file_upload(file_upload_id: int, db: Session = Depends(get_db)):
    """Delete a specific file upload record by ID"""
    db_file_upload = db.query(FileUploadModel).filter(FileUploadModel.id == file_upload_id).first()
    if not db_file_upload:
        raise HTTPException(status_code=404, detail="File upload not found")

    db.delete(db_file_upload)
    db.commit()
    return {"message": "File upload deleted successfully"}
