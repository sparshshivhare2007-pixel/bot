from pymongo import MongoClient
from chatbot.config import MONGO_URI

db = MongoClient(MONGO_URI)["chatbot_db"]
users = db["users"]

async def get_served_users():
    return [u async for u in users.find()]

async def is_user_exists(user_id: int):
    x = await users.find_one({"user_id": user_id})
    return bool(x)

async def add_user(user_id: int):
    if not await is_user_exists(user_id):
        await users.insert_one({"user_id": user_id})
