from fastapi import APIRouter, HTTPException
from typing import List
from .models import Item
from pydantic import BaseModel
from .database import r

from .models import PGItem
from sqlmodel import Session
from .database import postgres_engine


router = APIRouter()


class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


@router.post("/items/", response_model=ItemCreate)
async def create_item(item: ItemCreate):
    new_item = Item(**item.dict())
    await new_item.insert()
    return new_item


@router.get("/items/", response_model=List[ItemCreate])
async def get_items():
    items = await Item.find_all().to_list()
    return items


@router.get("/items/{item_id}", response_model=ItemCreate)
async def get_item(item_id: str):
    item = await Item.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/items/{item_id}", response_model=ItemCreate)
async def update_item(item_id: str, item_data: ItemCreate):
    item = await Item.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = item_data.name
    item.description = item_data.description
    item.price = item_data.price
    item.quantity = item_data.quantity
    await item.save()
    return item


@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    item = await Item.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await item.delete()
    return {"message": "Item deleted successfully"}


@router.post("/pgitems/")
async def create_pg_item(item: ItemCreate):
    new_pg_item = PGItem(**item.dict())
    with Session(postgres_engine) as session:
        session.add(new_pg_item)
        session.commit()
        session.refresh(new_pg_item)
    return new_pg_item


@router.get("/pgitems/", response_model=List[ItemCreate])
async def get_pg_items():
    with Session(postgres_engine) as session:
        items = session.query(PGItem).all()
        return items


@router.post("/user/{user_id}")
def create_user(user_id: str, user: ItemCreate):
    if r.exists(user_id):
        raise HTTPException(status_code=400, detail="User already exists")
    r.hset(user_id, mapping=user.dict())
    return {"message": "User created successfully"}


@router.get("/user/{user_id}")
def get_user(user_id: str):
    if not r.exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    user = r.hgetall(user_id)
    return user


@router.put("/user/{user_id}")
def update_user(user_id: str, user: ItemCreate):
    if not r.exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    r.hset(user_id, mapping=user.dict())
    return {"message": "User updated successfully"}


@router.delete("/user/{user_id}")
def delete_user(user_id: str):
    if not r.exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    r.delete(user_id)
    return {"message": "User deleted successfully"}
