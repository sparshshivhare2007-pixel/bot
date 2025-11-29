from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
chat_db = client["chatbot_db"]

# Collections
users = chat_db["users"]
sessions = chat_db["sessions"]  # optional, if chatbot uses session tracking

# ------------------- CHAT USER SYSTEM -------------------
def get_chat_user(user_id):
    user = users.find_one({"user_id": user_id})
    if not user:
        users.insert_one({
            "user_id": user_id,
            "messages": [],
            "joined": True
        })
        user = users.find_one({"user_id": user_id})
    return user

def add_message(user_id, message):
    users.update_one(
        {"user_id": user_id},
        {"$push": {"messages": message}},
        upsert=True
    )

# ------------------- UTILS -------------------
def is_user_exists(user_id):
    return users.find_one({"user_id": user_id}) is not None
