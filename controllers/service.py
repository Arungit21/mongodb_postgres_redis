from fastapi import APIRouter, HTTPException
from typing import List
from models.packages import Item, PGItem, ItemCreate
from services.controllers import (
    create_beanie_item, get_all_beanie_items, get_single_beanie_item, update_beanie_item, delete_beanie_item,
    create_pg_item_service, get_pg_items_service,
    create_user_redis, get_user_redis, update_user_redis, delete_user_redis
)

router = APIRouter()

# MongoDB Routes
@router.post("/items/", response_model=ItemCreate)
async def create_item(item: ItemCreate):
    return await create_beanie_item(item)

@router.get("/items/", response_model=List[ItemCreate])
async def get_items():
    return await get_all_beanie_items()

@router.get("/items/{item_id}", response_model=ItemCreate)
async def get_item(item_id: str):
    return await get_single_beanie_item(item_id)

@router.put("/items/{item_id}", response_model=ItemCreate)
async def update_item(item_id: str, item_data: ItemCreate):
    return await update_beanie_item(item_id, item_data)

@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    return await delete_beanie_item(item_id)


# PostgreSQL Routes
@router.post("/pgitems/")
async def create_pg_item(item: ItemCreate):
    return create_pg_item_service(item)

@router.get("/pgitems/", response_model=List[ItemCreate])
async def get_pg_items():
    return get_pg_items_service()


# Redis Routes
@router.post("/user/{user_id}")
def create_user(user_id: str, user: ItemCreate):
    return create_user_redis(user_id, user)

@router.get("/user/{user_id}")
def get_user(user_id: str):
    return get_user_redis(user_id)

@router.put("/user/{user_id}")
def update_user(user_id: str, user: ItemCreate):
    return update_user_redis(user_id, user)

@router.delete("/user/{user_id}")
def delete_user(user_id: str):
    return delete_user_redis(user_id)
