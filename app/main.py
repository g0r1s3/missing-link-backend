from fastapi import FastAPI
from app.api import items

app = FastAPI(
    title="Missing Link API",
    description="Das Backend für meine React-App",
    version="0.1.0",
)

app.include_router(items.router)

@app.get("/hello")
def hello():
    return {"msg": "Hello, FastAPI 👋"}
