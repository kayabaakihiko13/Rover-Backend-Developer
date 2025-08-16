from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime


from .utils import generate_uuid
from src.settings.db import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(String,primary_key=True,default=generate_uuid)
    firstname = Column(String(100),nullable=False)
    lastname = Column(String(100),nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(50),unique=True,nullable=False,index=True)
    password = Column(Text, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
