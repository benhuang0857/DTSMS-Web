from sqlalchemy import Column, BigInteger, Integer, String, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base
from enums import BasicStatus

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True, comment="用戶ID")
    account = Column(String(50), unique=True, index=True, comment="帳戶名")
    email = Column(String(255), unique=True, index=True, comment="用戶電子郵件")
    avatar = Column(String(255), nullable=True, comment="用戶頭像")
    real_name = Column(String(100), nullable=True, comment="真實姓名")
    organization = Column(String(100), nullable=True, comment="所屬組織")
    address = Column(String(255), nullable=True, comment="地址")
    mobile = Column(String(15), nullable=True, comment="手機號碼")
    password = Column(String(255), nullable=False, comment="密碼")
    status = Column(Enum(BasicStatus, name="basic_status"), nullable=False, comment="狀態")
    role_id = Column(BigInteger, ForeignKey('roles.id', ondelete='SET NULL'), nullable=True, comment="角色ID")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="創建時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")
    
    # relationship
    role = relationship("Role", backref="users")
    tickets = relationship("Ticket", back_populates="user", cascade="all, delete-orphan")
    uploaded_files = relationship("UploadedFile", back_populates="user", cascade="all, delete-orphan")

