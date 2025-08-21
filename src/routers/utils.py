from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from passlib.context import CryptContext
from src.settings.db import SessionLocal
from src.settings.config import settings


# pasword hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_pw,hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY_JWT, 
                             algorithm=settings.ALGORITHM)
    return encoded_jwt

