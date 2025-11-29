from pymongo import MongoClient
from chatbot.config import MONGO_URI

db = MongoClient(MONGO_URI)["chatbot_db"]
chatsdb = db["chats"]

async def get_served_chats():
    return [c async for c in chatsdb.find()]

async def is_served_chat(chat_id: int):
    x = await chatsdb.find_one({"chat_id": chat_id})
    return bool(x)

async def add_chat(chat_id: int):
    if not await is_served_chat(chat_id):
        await chatsdb.insert_one({"chat_id": chat_id})
