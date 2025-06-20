from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from models.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, comment="用戶ID")
    account = Column(String(50), unique=True, index=True, comment="帳戶名")
    email = Column(String(255), unique=True, index=True, comment="用戶電子郵件")
    avatar = Column(String(255), nullable=True, comment="用戶頭像")
    real_name = Column(String(100), nullable=True, comment="真實姓名")
    organization = Column(String(100), nullable=True, comment="所屬組織")
    address = Column(String(255), nullable=True, comment="地址")
    mobile = Column(String(15), nullable=True, comment="手機號碼")
    password = Column(String(255), nullable=False, comment="密碼")
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='SET NULL'), nullable=True, comment="角色ID")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="創建時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")
