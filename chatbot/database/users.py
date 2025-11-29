from . import users_col  # database/__init__.py me defined collection

# -------------------- USER HELPERS --------------------

async def is_served_user(user_id: int) -> bool:
    """
    Checks if a user_id is already served.
    """
    user = await users_col.find_one({"user_id": user_id})
    return bool(user)

async def get_served_users() -> list:
    """
    Returns a list of all served users (user_id > 0).
    """
    users_list = []
    async for user in users_col.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def add_served_user(user_id: int):
    """
    Adds a new user_id to served users.
    """
    if await is_served_user(user_id):
        return
    return await users_col.insert_one({"user_id": user_id})
