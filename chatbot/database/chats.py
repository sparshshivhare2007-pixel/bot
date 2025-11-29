from . import chats_col  # database/__init__.py me defined collection

# -------------------- CHAT HELPERS --------------------

async def get_served_chats() -> list:
    """
    Returns a list of all served chats (chat_id < 0).
    """
    chats_cursor = chats_col.find({"chat_id": {"$lt": 0}})
    chats_list = []
    async for chat in chats_cursor:
        chats_list.append(chat)
    return chats_list

async def is_served_chat(chat_id: int) -> bool:
    """
    Checks if a chat_id is already served.
    """
    chat = await chats_col.find_one({"chat_id": chat_id})
    return bool(chat)

async def add_served_chat(chat_id: int):
    """
    Adds a new chat_id to served chats.
    """
    if await is_served_chat(chat_id):
        return
    return await chats_col.insert_one({"chat_id": chat_id})

async def remove_served_chat(chat_id: int):
    """
    Removes a chat_id from served chats.
    """
    if not await is_served_chat(chat_id):
        return
    return await chats_col.delete_one({"chat_id": chat_id})
