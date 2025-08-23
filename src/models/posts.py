from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from src.settings.db import Base
from src.models.utils import generate_uuid

# models/post.py
class Post(Base):
    __tablename__ = "post"

    post_id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    image_url = Column(String, nullable=False)
    create_at = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="posts")

    # harus "Result" (singular), dan back_populates harus match dengan di Result
    results = relationship("Result", back_populates="post", cascade="all, delete")
