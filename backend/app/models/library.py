from sqlalchemy import Column, BigInteger, Integer, String, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base
from enums import BasicStatus

class Library(Base):
    __tablename__ = 'libraries'

    id = Column(BigInteger, primary_key=True, index=True, comment="Library ID")
    name = Column(String(100), nullable=False, unique=True, comment="Library Name")
    protocal = Column(String(50), nullable=True, comment="Protocol Type")
    baudrate = Column(Integer, nullable=True, comment="Baudrate")
    parity = Column(String(10), nullable=True, comment="Parity Type")
    stopbits = Column(Integer, nullable=True, comment="Stop Bits")
    bytesize = Column(Integer, nullable=True, comment="Byte Size")
    host = Column(String(100), nullable=True, comment="Host Address")
    port = Column(Integer, nullable=True, comment="Port Number")
    certfile = Column(String(255), nullable=True, comment="Certificate File Path")
    description = Column(String(255), nullable=True, comment="Library Description")
    status = Column(Enum(BasicStatus, name="basic_status"), nullable=False, comment="狀態")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="Creation Time")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="Update Time")

    # Relationships
    recipes = relationship("Recipe", back_populates="library", lazy="select")