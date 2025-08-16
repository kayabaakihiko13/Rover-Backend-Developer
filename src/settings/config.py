from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env_name = 'env.local'
    baser