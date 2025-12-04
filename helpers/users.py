from .db import users
from datetime import datetime

def get_user(user_id: int):
    user = users.find_one({"user_id": user_id})
    if not user:
        user = {"user_id": user_id, "balance": 0, "kills": 0, "last_daily": None}
        users.insert_one(user)
    return user

def update_user(user_id: int, data: dict):
    users.update_one({"user_id": user_id}, {"$set": data})
