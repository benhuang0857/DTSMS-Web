from sqlalchemy import Column, BigInteger, Integer, String, TIMESTAMP, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base
from enums import BasicStatus

class Library(Base):
    __tablename__ = 'libraries'

    id = Column(BigInteger, primary_key=True, index=True, comment="Library ID")
    name = Column(String(100), nullable=False, unique=True, comment="Library Name")
    api_endpoint = Column(String(500), nullable=False, comment="API Endpoint URL")
    docker_image = Column(String(255), nullable=True, comment="Docker Image Name (Optional for custom deployments)")
    docker_tag = Column(String(100), nullable=True, default='latest', comment="Docker Image Tag")
    api_key = Column(String(255), nullable=True, comment="API Authentication Key")
    api_headers = Column(JSON, nullable=True, comment="Additional API Headers")
    timeout_seconds = Column(Integer, nullable=True, default=30, comment="API Request Timeout")
    retry_count = Column(Integer, nullable=True, default=3, comment="API Request Retry Count")
    docker_env_vars = Column(JSON, nullable=True, comment="Docker Environment Variables")
    docker_ports = Column(JSON, nullable=True, comment="Docker Port Mappings")
    docker_volumes = Column(JSON, nullable=True, comment="Docker Volume Mappings")
    health_check_endpoint = Column(String(500), nullable=True, comment="Health Check API Endpoint")
    description = Column(String(500), nullable=True, comment="Library Description")
    status = Column(Enum(BasicStatus, name="basic_status"), nullable=False, comment="狀態")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="Creation Time")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="Update Time")

    # Relationships
    actions = relationship("LibraryAction", back_populates="library", lazy="select", cascade="all, delete-orphan")