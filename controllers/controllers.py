from fastapi import APIRouter
from typing import List
from models.packages import ItemCreate
from services.services import (
    create_beanie_item, get_all_beanie_items, get_single_beanie_item, update_beanie_item, delete_beanie_item,
    create_pg_item_service, get_pg_items_service, update_pg_item_service, delete_pg_item_service, create_user_redis, get_user_redis, update_user_redis, delete_user_redis
)

router = APIRouter()


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

# PostgreSQL + Redis Routes


@router.post("/pgitems/")
async def create_pg_item(item: ItemCreate):
    return create_pg_item_service(item)


@router.get("/pgitems/", response_model=List[dict])
async def get_pg_items():
    return get_pg_items_service()


@router.put("/pgitems/{item_name}")
async def update_pg_item(item_name: str, item: ItemCreate):
    return update_pg_item_service(item_name, item)


@router.delete("/pgitems/{item_name}")
async def delete_pg_item(item_name: str):
    return delete_pg_item_service(item_name)


@router.get("/user/{user_id}")
def get_user(user_id: str):
    return get_user_redis(user_id)


@router.put("/user/{user_id}")
def update_user(user_id: str, user: ItemCreate):
    return update_user_redis(user_id, user)


@router.delete("/user/{user_id}")
def delete_user(user_id: str):
    return delete_user_redis(user_id)
