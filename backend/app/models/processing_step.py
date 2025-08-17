from sqlalchemy import Column, BigInteger, Integer, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base

class ProcessingStep(Base):
    __tablename__ = 'processing_steps'
    
    id = Column(BigInteger, primary_key=True, index=True, comment="處理步驟ID")
    autoflow_id = Column(BigInteger, ForeignKey('autoflows.id'), nullable=True, comment="關聯掃描自動化腳本ID")
    library_action_id = Column(BigInteger, ForeignKey('library_actions.id'), nullable=False, comment="關聯 Library Action ID")
    name = Column(String(50), nullable=False, comment="步驟名稱")
    description = Column(String(255), nullable=True, comment="步驟描述")
    execution_order = Column(Integer, nullable=False, server_default="1", comment="執行順序，數字相同表示可同時執行")
    parameters = Column(JSON, nullable=True, comment="步驟執行參數")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="建立時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")

    # Relationships
    autoflow = relationship("Autoflow", back_populates="processing_steps", lazy="joined")
    library_action = relationship("LibraryAction", back_populates="processing_steps", lazy="joined")
    file_trackings = relationship("FileTracking", back_populates="processing_step", lazy="select")