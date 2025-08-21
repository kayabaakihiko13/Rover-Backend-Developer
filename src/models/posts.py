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
    create_at = Column(DateTime, default=datetime.utcnow)

    # 🔑 harus cocok
    user = relationship("User", back_populates="posts")

    # results = relationship("Results", back_populates="post", cascade="all, delete")
