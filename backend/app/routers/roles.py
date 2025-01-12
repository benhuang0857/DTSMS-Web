from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Role as RoleModel  # Assuming the Role model matches the schema
from schemas import RoleCreate, RoleUpdate, Role  # Ensure these schemas align with the schema
from database import get_db

router = APIRouter()

# Create a new role
@router.post("/", response_model=Role)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    """Add a new role"""
    # Check if title is unique
    existing_role = db.query(RoleModel).filter(RoleModel.title == role.title).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role title already exists")

    db_role = RoleModel(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# Get all roles (with pagination)
@router.get("/", response_model=list[Role])
def get_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Retrieve all roles (paginated)"""
    return db.query(RoleModel).offset(skip).limit(limit).all()

# Get a specific role by ID
@router.get("/{role_id}", response_model=Role)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific role by ID"""
    db_role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

# Update a specific role by ID
@router.put("/{role_id}", response_model=Role)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    """Update a specific role by ID"""
    db_role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Update only provided fields
    for key, value in role.dict(exclude_unset=True).items():
        setattr(db_role, key, value)

    db.commit()
    db.refresh(db_role)
    return db_role

# Delete a specific role by ID
@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    """Delete a specific role by ID"""
    db_role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    db.delete(db_role)
    db.commit()
    return {"message": "Role deleted successfully"}
