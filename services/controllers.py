from fastapi import HTTPException
from models.packages import Item, PGItem, ItemCreate
from database.database import postgres_engine, r
from sqlmodel import Session

# MongoDB (Beanie) Services
async def create_beanie_item(item: ItemCreate):
    new_item = Item(**item.dict())
    await new_item.insert()
    return new_item

async def get_all_beanie_items():
    return await Item.find_all().to_list()

async def get_single_beanie_item(item_id: str):
    item = await Item.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

async def update_beanie_item(item_id: str, item_data: ItemCreate):
    item = await Item.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = item_data.name
    item.description = item_data.description
    item.price = item_data.price
    item.quantity = item_data.quantity
    await item.save()
    return item

async def delete_beanie_item(item_id: str):
    item = await Item.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await item.delete()
    return {"message": "Item deleted successfully"}


# PostgreSQL Services
def create_pg_item_service(item: ItemCreate):
    new_pg_item = PGItem(**item.dict())
    with Session(postgres_engine) as session:
        session.add(new_pg_item)
        session.commit()
        session.refresh(new_pg_item)
    return new_pg_item

def get_pg_items_service():
    with Session(postgres_engine) as session:
        return session.query(PGItem).all()


# Redis Services
def create_user_redis(user_id: str, user: ItemCreate):
    if r.exists(user_id):
        raise HTTPException(status_code=400, detail="User already exists")
    r.hset(user_id, mapping=user.dict())
    return {"message": "User created successfully"}

def get_user_redis(user_id: str):
    if not r.exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return r.hgetall(user_id)

def update_user_redis(user_id: str, user: ItemCreate):
    if not r.exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    r.hset(user_id, mapping=user.dict())
    return {"message": "User updated successfully"}

def delete_user_redis(user_id: str):
    if not r.exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    r.delete(user_id)
    return {"message": "User deleted successfully"}
