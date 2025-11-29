from pyrogram import filters
from chatbot import ChatBot
from chatbot.database.chats import get_served_chats
from chatbot.database.users import get_served_users
from config import OWNER

@ChatBot.on_message(filters.command("stats") & filters.user(OWNER))
async def stats(_, message):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    await message.reply_text(f"Total Stats:\nChats: {chats}\nUsers: {users}")
