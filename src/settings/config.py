from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_DEV :str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    ALGORITHM:str
    SECRET_KEY_JWT:str
    class Config:
        env_file = "src\.env.local"

settings = Settings()