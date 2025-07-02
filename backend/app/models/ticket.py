from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func, Enum
from sqlalchemy.ext.declarative import declarative_base
from enums import BasicStatus

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(BigInteger, primary_key=True)
    ticket_num = Column(String(255), nullable=False, unique=True, comment="單號")
    status = Column(Enum(BasicStatus, name="basic_status"), nullable=False, comment="狀態")
    created_time = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
