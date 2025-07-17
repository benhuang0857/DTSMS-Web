from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    TIMESTAMP,
    Enum,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base
from enums import TrackingStatus

class FileTracking(Base):
    __tablename__ = 'file_trackings'
    
    id = Column(BigInteger, primary_key=True, index=True, comment="主鍵ID")
    tracking_id = Column(UUID(as_uuid=True), unique=True, nullable=False, server_default=func.text("gen_random_uuid()"), comment="唯一追蹤ID")
    uploaded_file_id = Column(BigInteger, ForeignKey('uploaded_files.id'), nullable=False, comment="關聯檔案ID")
    step_id = Column(BigInteger, ForeignKey('processing_steps.id'), nullable=False, comment="關聯處理步驟ID")
    start_time = Column(TIMESTAMP, nullable=False, comment="開始時間")
    end_time = Column(TIMESTAMP, nullable=True, comment="結束時間")
    result = Column(String(255), nullable=True, comment="處理結果")
    status = Column(Enum(TrackingStatus, name="tracking_status"), nullable=False, comment="狀態")
    note = Column(Text, nullable=True, comment="備註")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="建立時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")

    # Relationships
    uploaded_file = relationship("UploadedFile", back_populates="file_trackings", lazy="joined")
    processing_step = relationship("ProcessingStep", back_populates="file_trackings", lazy="joined")
