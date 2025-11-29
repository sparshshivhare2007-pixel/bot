from . import usersdb

async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def is_served_user(user_id: int) -> bool:
    return bool(await usersdb.find_one({"user_id": user_id}))

async def add_served_user(user_id: int):
    if not await is_served_user(user_id):
        await usersdb.insert_one({"user_id": user_id})
