from sqlalchemy import Column, BigInteger, Integer, String, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.sql import func
from models.base import Base
from enums import TrackingStatus

class UploadedFile(Base):
    __tablename__ = 'uploaded_files'
    
    id = Column(BigInteger, primary_key=True, index=True, comment="檔案上傳ID")
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='SET NULL'), nullable=False, comment="用戶ID")
    ticket_num = Column(String(255), nullable=False, unique=True, comment="單號")
    name = Column(String(255), nullable=False, comment="檔案名稱")
    ftype = Column(String(50), nullable=False, comment="檔案類型")
    fsize = Column(BigInteger, nullable=False, comment="檔案大小（位元組）")
    unzip_password = Column(String(255), nullable=True, comment="解壓縮密碼")
    description = Column(String(255), nullable=True, comment="檔案描述")
    status = Column(Enum(TrackingStatus, name="tracking_status"), nullable=False, comment="狀態")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="建立時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")
