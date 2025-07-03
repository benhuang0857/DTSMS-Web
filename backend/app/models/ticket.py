from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enums import BasicStatus
from models.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='SET NULL'), nullable=True, comment="用戶ID")
    code = Column(String(255), nullable=False, unique=True, comment="單號")
    exp_start_time = Column(TIMESTAMP, nullable=True, comment="期限起始時間")
    exp_end_time = Column(TIMESTAMP, nullable=True, comment="期限結束時間")
    status = Column(Enum(BasicStatus, name="basic_status"), nullable=False, comment="狀態")
    created_time = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    # relationship
    user = relationship("User", back_populates="tickets")
    uploaded_file = relationship("UploadedFile", back_populates="ticket", uselist=False, cascade="all, delete-orphan")

