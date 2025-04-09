from beanie import Document
from pydantic import BaseModel


from typing import Optional
from pydantic import BaseModel


from beanie import Document
from sqlmodel import SQLModel, Field
from typing import Optional


class Item(Document):
    name: str
    description: str
    price: float
    quantity: int

    class Settings:
        collection = "items"
        
        
        
        
        


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
    
    
    
    
class User(BaseModel):
    name: str
    age: int
    email: str