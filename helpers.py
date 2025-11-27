from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import random

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["economy_bot"]
users = db["users"]
groups = db["groups"]
couples = db["couples"]


# ----------------- DB Helper Functions -----------------
def get_user(user_id):
    user = users.find_one({"user_id": user_id})
    if not user:
        users.insert_one({
            "user_id": user_id,
            "balance": 0,
            "kills": 0,
            "killed": False,
        })
        user = users.find_one({"user_id": user_id})
    return user

def is_group_open(chat_id):
    group = groups.find_one({"chat_id": chat_id})
    return group.get("open", True) if group else True

def set_group_status(chat_id, status: bool):
    groups.update_one({"chat_id": chat_id}, {"$set": {"open": status}}, upsert=True)

def random_percentage():
    return random.randint(0, 100)
