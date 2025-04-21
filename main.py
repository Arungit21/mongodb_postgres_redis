from fastapi import FastAPI
from controllers.controllers import router
from database.database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(router)
