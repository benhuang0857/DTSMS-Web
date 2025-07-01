from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from models.base import Base

class WebSetting(Base):
    __tablename__ = 'web_settings'

    id = Column(BigInteger, primary_key=True, index=True, comment="網站設定ID")
    key = Column(String(255), nullable=False, unique=True, comment="網站設定鍵")
    name = Column(String(255), nullable=False, comment="網站設定名稱")
    description = Column(String(255), nullable=True, comment="網站設定描述")
    value = Column(Text, nullable=False, comment="網站設定值")
    status = Column(String(255), nullable=False, comment="網站設定狀態")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="創建時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")