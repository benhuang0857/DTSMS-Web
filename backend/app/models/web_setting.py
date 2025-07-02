from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP, Enum
from sqlalchemy.sql import func
from models.base import Base
from enums import WebSettingStatus

class WebSetting(Base):
    __tablename__ = 'web_settings'

    id = Column(BigInteger, primary_key=True, index=True, comment="網站設定ID")
    key = Column(String(255), nullable=False, unique=True, comment="網站設定鍵")
    name = Column(String(255), nullable=False, comment="網站設定名稱")
    description = Column(String(255), nullable=True, comment="網站設定描述")
    value = Column(Text, nullable=False, comment="網站設定值")
    status = Column(Enum(WebSettingStatus, name="web_setting_status"), nullable=False, comment="狀態")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="創建時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")