from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey, Enum, JSON, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base
from enums import BasicStatus

class LibraryAction(Base):
    __tablename__ = 'library_actions'
    
    id = Column(BigInteger, primary_key=True, index=True, comment="Library Action ID")
    library_id = Column(BigInteger, ForeignKey('libraries.id', ondelete='CASCADE'), nullable=False, comment="Library ID")
    name = Column(String(100), nullable=False, comment="Action Name (e.g., '一般掃描', '進階掃描')")
    api_path = Column(String(200), nullable=False, comment="API Path (e.g., '/scan/basic', '/scan/advanced')")
    http_method = Column(String(10), nullable=False, default='POST', comment="HTTP Method (GET, POST, PUT, DELETE)")
    request_schema = Column(JSON, nullable=True, comment="Request body schema/parameters")
    response_schema = Column(JSON, nullable=True, comment="Expected response schema")
    description = Column(String(500), nullable=True, comment="Action Description")
    execution_order = Column(Integer, nullable=True, comment="Suggested execution order in workflows")
    status = Column(Enum(BasicStatus, name="basic_status"), nullable=False, server_default="active", comment="狀態")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="Creation Time")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="Update Time")

    # Relationships
    library = relationship("Library", back_populates="actions", lazy="joined")
    processing_steps = relationship("ProcessingStep", back_populates="library_action", lazy="select")