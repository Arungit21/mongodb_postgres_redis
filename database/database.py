from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.packages import Item

import redis
r = redis.Redis(host="localhost", port=6379)

from sqlmodel import SQLModel, create_engine, Session

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "fastapi_microservices"

POSTGRES_URL = "postgresql://postgres:root@localhost/john"
postgres_engine = create_engine(POSTGRES_URL, echo=True)

async def init_db():
    # MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    database = client[DATABASE_NAME]
    await init_beanie(database, document_models=[Item])
    
    # PostgreSQL
    SQLModel.metadata.create_all(postgres_engine)
