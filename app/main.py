# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import items
from app.api.v1.routers import auth  # <<< NEU/
from app.api.v1.routers import bikes as bikes_router  # neu
import app.api.v1.routers.maintenances as maint_router

app = FastAPI(
    title="Missing Link API",
    description="Mein FastAPI-Backend (Auth + Items)",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Unbedingt BEIDE Router registrieren:
app.include_router(auth.router, prefix="/api/v1")   # <<< wichtig
app.include_router(items.router, prefix="/api/v1")
app.include_router(bikes_router.router, prefix="/api/v1")  # neu

app.include_router(maint_router.router, prefix="/api/v1")     # <-- neu

