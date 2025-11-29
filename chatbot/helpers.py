# chat/helpers.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
chat_db = client["chat_bot"]

# Messages / users collection
chat_users = chat_db["users"]

def get_chat_user(user_id):
    user = chat_users.find_one({"user_id": user_id})
    if not user:
        chat_users.insert_one({"user_id": user_id, "messages": []})
        user = chat_users.find_one({"user_id": user_id})
    return user

def add_message(user_id, message):
    chat_users.update_one({"user_id": user_id}, {"$push": {"messages": message}}, upsert=True)

def is_user_exists(user_id):
    return chat_users.find_one({"user_id": user_id}) is not None
