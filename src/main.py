from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.routers.users import router as user_router
from src.settings.db import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# cors default setups

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Bisa pakai ["*"] kalau mau semua origin
    allow_credentials=True,
    allow_methods=["*"],            # Izinkan semua method (GET, POST, dll)
    allow_headers=["*"],            # Izinkan semua headers
)
app.include_router(user_router)
