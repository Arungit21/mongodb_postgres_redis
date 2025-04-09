from fastapi import FastAPI
from .database import init_db
from .routes import router

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(router)