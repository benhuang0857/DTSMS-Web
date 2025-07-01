from sqlalchemy import Column, BigInteger, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from models.base import Base

class Role(Base):
    __tablename__ = 'roles'

    id = Column(BigInteger, primary_key=True, index=True, comment="角色ID")
    name = Column(String(50), unique=True, nullable=False, comment="角色名稱")
    description = Column(String(255), nullable=True, comment="角色描述")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="創建時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")
