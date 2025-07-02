from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Ticket as TicketModel
from schemas import TicketCreate, TicketUpdate, Ticket
from database import get_db
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

# 創建票券
@router.post("/", response_model=Ticket)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """新增票券"""
    existing_ticket = db.query(TicketModel).filter(TicketModel.ticket_num == ticket.ticket_num).first()
    if existing_ticket:
        raise HTTPException(status_code=400, detail="票號已存在")

    db_ticket = TicketModel(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# 獲取所有票券（分頁）
@router.get("/", response_model=list[Ticket])
def get_tickets(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """查詢所有票券（分頁）"""
    return db.query(TicketModel).offset(skip).limit(limit).all()

# 根據 ID 取得票券
@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """根據 ID 取得票券"""
    db_ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="票券未找到")
    return db_ticket

# 根據 ID 更新票券
@router.put("/{ticket_id}", response_model=Ticket)
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """根據 ID 更新票券"""
    db_ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="票券未找到")

    for key, value in ticket.dict(exclude_unset=True).items():
        setattr(db_ticket, key, value)

    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# 根據 ID 刪除票券
@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """根據 ID 刪除票券"""
    db_ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="票券未找到")

    db.delete(db_ticket)
    db.commit()
    return {"message": "票券已成功刪除"}
