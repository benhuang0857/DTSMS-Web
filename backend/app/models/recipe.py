from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base
from enums import BasicStatus

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(BigInteger, primary_key=True, index=True, comment="站點自動化腳本ID")
    name = Column(String(255), nullable=False, comment="腳本名稱")
    description = Column(Text, nullable=True, comment="腳本描述")
    status = Column(Enum(BasicStatus, name="basic_status"), nullable=False, server_default="active", comment="狀態")
    allow_parallel_autoflows = Column(Boolean, nullable=False, server_default="false", comment="是否允許Autoflow並行執行")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="創建時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")

    # Relationships
    recipe_steps = relationship("RecipeStep", back_populates="recipe", lazy="select", cascade="all, delete-orphan")
    autoflows = relationship("Autoflow", back_populates="recipe", lazy="select")

class RecipeStep(Base):
    __tablename__ = 'recipe_steps'
    
    id = Column(BigInteger, primary_key=True, index=True, comment="站點腳本步驟ID")
    recipe_id = Column(BigInteger, ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, comment="腳本ID")
    number = Column(Integer, nullable=False, comment="步驟序號")
    action = Column(String(50), nullable=False, comment="執行動作")
    parameters = Column(JSON, nullable=True, comment="參數")
    status = Column(Enum(BasicStatus, name="basic_status"), nullable=False, server_default="active", comment="狀態")
    created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False, comment="創建時間")
    updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間")

    # Relationships
    recipe = relationship("Recipe", back_populates="recipe_steps", lazy="joined")