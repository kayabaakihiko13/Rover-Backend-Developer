from pydantic import BaseModel
from datetime import datetime
from typing import Dict,List


class ResultCreaee(BaseModel):
    class_ids:List[int]
    socres:List[float]


class ResultResponseBase(BaseModel):
    result_id: str
    post_id: str
    image_url: str
    result: Dict[str,object]   # kalau JSON bebas isinya, bisa pakai Any
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # biar bisa langsung return dari ORM
