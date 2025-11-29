from . import chatsdb

async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    return bool(chat)

async def add_chat(chat_id: int):
    if not await is_served_chat(chat_id):
        await chatsdb.insert_one({"chat_id": chat_id})

async def get_served_chats():
    return [c async for c in chatsdb.find()]
