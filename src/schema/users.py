from pydantic import BaseModel,EmailStr
from datetime import datetime


class RegisterRequest(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: str
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    create_at: datetime
    update_at: datetime

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

