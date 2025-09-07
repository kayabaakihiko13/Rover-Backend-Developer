from pydantic import BaseModel
from datetime import datetime


class PostCreateRequest(BaseModel):
    user_id:str
    image_url:str

class PostResponse(BaseModel):
    post_id :str
    user_id :str
    image_url : str

    class Config:
        orm_mode = True

