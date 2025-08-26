# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import items

app = FastAPI(
    title="Missing Link API",
    description="Mein FastAPI-Backend (In-Memory CRUD als Start)",
    version="0.2.0",
)

# React-Dev-Server zulassen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routen registrieren
app.include_router(items.router, prefix="/api/v1")

# Health-Check
@app.get("/healthz")
def health():
    return {"ok": True}
