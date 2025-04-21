from beanie import Document
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional


# MongoDB Document
class Item(Document):
    name: str
    description: str
    price: float
    quantity: int

    class Settings:
        collection = "items"

# PostgreSQL Table
class PGItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    quantity: int

# Shared Pydantic Model
class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
