from sqlalchemy import Column, Integer, BigInteger, String, Text, JSON, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    avatar = Column(String(255), nullable=True)
    real_name = Column(String(100), nullable=True)
    organization = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    mobile = Column(String(15), nullable=True)
    password = Column(String(255), nullable=False)
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

class FileUpload(Base):
    __tablename__ = 'file_uploads'

    id = Column(BigInteger, primary_key=True, index=True)
    tracking_num = Column(String(100), unique=True, index=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    token = Column(String(255), nullable=True)
    status = Column(String(50), server_default='process', nullable=False)
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

class Report(Base):
    __tablename__ = 'reports'

    id = Column(BigInteger, primary_key=True, index=True)
    file_upload_id = Column(BigInteger, ForeignKey('file_uploads.id', ondelete='CASCADE'))
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    result = Column(JSON, nullable=True)
    token = Column(String(255), nullable=True)
    status = Column(String(50), server_default="process", nullable=False)
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

class Log(Base):
    __tablename__ = 'logs'

    id = Column(BigInteger, primary_key=True, index=True)
    level = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    status = Column(String(50), server_default="active", nullable=False)
    note = Column(String(255), server_default="active", nullable=True)
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

class Automation(Base):
    __tablename__ = "automations"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    note = Column(String(255), server_default="active")
    status = Column(String(50), server_default="process")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

class Action(Base):
    __tablename__ = "actions"

    id = Column(BigInteger, primary_key=True, index=True)
    automation_id = Column(BigInteger, ForeignKey("automations.id", ondelete="SET NULL"), nullable=True)
    api_type = Column(String(255), nullable=True)
    endpoint = Column(String(255), nullable=True)
    command = Column(JSON, nullable=True)
    note = Column(String(255), server_default="active")
    status = Column(String(50), server_default="process")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
