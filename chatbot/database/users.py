from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["chatbot"]
usersdb = db["users"]

async def get_user(user_id):
    user = usersdb.find_one({"user_id": user_id})
    if not user:
        usersdb.insert_one({"user_id": user_id, "messages": 0})
        user = usersdb.find_one({"user_id": user_id})
    return user
