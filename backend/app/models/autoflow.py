from sqlalchemy import Column, BigInteger, String, Text, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base
from enums import BasicStatus

class Autoflow(Base):
    __tablename__ = 'autoflows'
    
    id = Column(BigInteger, primary_key=True, index=True, comment="掃描自動化流程ID")
    recipe_id = Column(BigInteger, ForeignKey('recipes.id', ondelete='SET NULL'), nullable=True, comment="腳本ID")
    name = Column(String(255), nullable=False, comment="流程名稱")
    description = Column(Text, nullable=True, comment="流程描述")
    status = Column(Enum(BasicStatus, name="basic_status"), nullable=False, server_default="active", comment="狀態")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="創建時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")

    # Relationships
    recipe = relationship("Recipe", back_populates="autoflows", lazy="joined")
    processing_steps = relationship("ProcessingStep", back_populates="autoflow", lazy="select")