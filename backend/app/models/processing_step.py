from sqlalchemy import Column, BigInteger, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from models.base import Base

class ProcessingStep(Base):
    __tablename__ = 'processing_steps'
    
    id = Column(BigInteger, primary_key=True, index=True, comment="處理步驟ID")
    step_name = Column(String(50), nullable=False, comment="步驟名稱")
    description = Column(String(255), nullable=True, comment="步驟描述")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="建立時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")