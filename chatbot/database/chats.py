from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["chatbot"]
chatsdb = db["chats"]

async def save_chat(chat_id):
    if not chatsdb.find_one({"chat_id": chat_id}):
        chatsdb.insert_one({"chat_id": chat_id})
