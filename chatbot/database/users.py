from . import usersdb

async def is_user_exists(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    return bool(user)

async def add_user(user_id: int):
    if not await is_user_exists(user_id):
        await usersdb.insert_one({"user_id": user_id})

async def get_served_users():
    return [u async for u in usersdb.find()]
