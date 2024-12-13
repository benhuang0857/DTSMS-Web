# models.py
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    avatar = Column(String)
    real_name = Column(String)
    organization = Column(String)
    address = Column(String)
    mobile = Column(String)
    password = Column(String)
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

class FileUpload(Base):
    __tablename__ = 'file_uploads'

    id = Column(Integer, primary_key=True, index=True)
    tracking_num = Column(String, unique=True, index=True)
    user = Column(String, unique=True)
    token = Column(String, nullable=True)
    status = Column(String, server_default='process')
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)