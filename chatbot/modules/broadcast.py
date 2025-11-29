import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from chatbot import ChatBot
from chatbot.database.chats import get_served_chats
from chatbot.database.users import get_served_users
from config import OWNER_ID

@ChatBot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(_, message: Message):
    reply = message.reply_to_message
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    if not reply and not text:
        return await message.reply_text("❖ Reply to a message or provide text to broadcast.")

    progress_msg = await message.reply_text("❖ Broadcasting message... Please wait")
    sent_groups, sent_users, failed, pinned = 0, 0, 0, 0

    chats_data = await get_served_chats()
    users_data = await get_served_users()

    recipients = [cha]()
