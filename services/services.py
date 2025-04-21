from fastapi import HTTPException
from models.packages import Item, PGItem, ItemCreate
from database.database import postgres_engine, r
from sqlmodel import Session
from sqlalchemy import text


# # ---------- MongoDB (Beanie) ----------
async def create_beanie_item(item: ItemCreate):
    return await Item(**item.dict()).insert()


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

    await Item.find(Item.id == item_id).update(
        {
            "$set": {
                "name": item_data.name,
                "description": item_data.description,
                "price": item_data.price,
                "quantity": item_data.quantity
            }
        }
    )
    return await Item.get(item_id)


async def delete_beanie_item(item_id: str):
    item = await Item.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await item.delete()
    return {"message": "Item deleted successfully"}

# ---------- PostgreSQL + Redis Sync ----------


def create_pg_item_service(item: ItemCreate):
    with Session(postgres_engine) as session:
        session.execute(
            text("""
                INSERT INTO pgitem (name, description, price, quantity)
                VALUES (:name, :description, :price, :quantity)
            """),
            {
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "quantity": item.quantity
            }
        )
        session.commit()

    # Sync to Redis
    r.hset(item.name, mapping=item.dict())
    return {"message": "PG item created and synced to Redis successfully"}


def get_pg_items_service():
    cached_keys = r.keys("*")
    if cached_keys:
        items = []
        for key in cached_keys:
            raw = r.hgetall(key)
            item = {k.decode(): float(v.decode()) if k.decode() in [
                "price", "quantity"] else v.decode() for k, v in raw.items()}
            items.append(item)
        return items

    # If Redis is empty, fetch from PG and populate Redis
    with Session(postgres_engine) as session:
        result = session.execute(text("SELECT * FROM pgitem"))
        rows = result.fetchall()
        for row in rows:
            r.hset(row.name, mapping={
                "name": row.name,
                "description": row.description,
                "price": row.price,
                "quantity": row.quantity
            })
        return [dict(row) for row in rows]


def update_pg_item_service(item_name: str, updated_data: ItemCreate):
    with Session(postgres_engine) as session:
        session.execute(
            text("""
                UPDATE pgitem
                SET description = :description,
                    price = :price,
                    quantity = :quantity
                WHERE name = :name
            """),
            {
                "name": item_name,
                "description": updated_data.description,
                "price": updated_data.price,
                "quantity": updated_data.quantity
            }
        )
        session.commit()

    # Sync to Redis
    r.hset(item_name, mapping=updated_data.dict())
    return {"message": "PG item updated and synced to Redis"}


def delete_pg_item_service(item_name: str):
    with Session(postgres_engine) as session:
        session.execute(
            text("DELETE FROM pgitem WHERE name = :name"),
            {"name": item_name}
        )
        session.commit()

    # Remove from Redis
    if r.exists(item_name):
        r.delete(item_name)

    return {"message": "PG item deleted from PostgreSQL and Redis"}


# ---------- Redis (Direct Query-Like Style) ----------
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
