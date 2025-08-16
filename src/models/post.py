from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from src.settings import Base
from utils import generate_uuid

class Post(Base):
    __tablename__ = "post"

    post_id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    image_url = Column(String, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts")
    results = relationship("Result", back_populates="post", cascade="all, delete")
