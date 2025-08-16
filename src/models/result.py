from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from src.settings import Base
from utils import generate_uuid

class Result(Base):
    __tablename__ = "result"

    result_id = Column(String, primary_key=True, default=generate_uuid)
    post_id = Column(String, ForeignKey("post.post_id"), nullable=False)
    result = Column(JSON, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="results")