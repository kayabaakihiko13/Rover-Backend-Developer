from sqlalchemy import Column, String, ForeignKey, DateTime,JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from src.settings.db import Base
from src.models.utils import generate_uuid

class Result(Base):
    __tablename__ = "results"

    result_id = Column(String, primary_key=True, default=generate_uuid)
    post_id = Column(String, ForeignKey("post.post_id"), nullable=False)
    result = Column(JSON, nullable=False)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)

    # back_populates harus sama kayak di Post
    post = relationship("Post", back_populates="results")


