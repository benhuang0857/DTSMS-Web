from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import Ticket as TicketModel
from schemas import TicketCreate, TicketUpdate, Ticket
from database import get_db
from routers.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()

@router.post("/", response_model=Ticket)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    try:
        existing_ticket = db.query(TicketModel).filter(TicketModel.code == ticket.code).first()
        if existing_ticket:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "票號已存在"}
            )

        db_ticket = TicketModel(**ticket.dict())
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫完整性錯誤: {str(e)}"}
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.get("/", response_model=list[Ticket])
def get_tickets(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    try:
        tickets = (
            db.query(TicketModel)
            .options(joinedload(TicketModel.user))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return tickets
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    try:
        db_ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
        if not db_ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "票券未找到"}
            )
        return db_ticket
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.put("/{ticket_id}", response_model=Ticket)
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    try:
        db_ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
        if not db_ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "票券未找到"}
            )

        for key, value in ticket.dict(exclude_unset=True).items():
            setattr(db_ticket, key, value)

        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )

@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    try:
        db_ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
        if not db_ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "票券未找到"}
            )

        db.delete(db_ticket)
        db.commit()
        return {"code": 200, "message": "票券已成功刪除"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"資料庫錯誤: {str(e)}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"伺服器內部錯誤: {str(e)}"}
        )
