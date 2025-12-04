from pyrogram import filters
from pyrogram.types import Message
from helpers.users import users
from main import app

@app.on_message(filters.command("topkill"))
async def topkill(client, message: Message):
    top_users = users.find().sort("kills", -1).limit(10)
    text = "🏆 Top 10 Users by Kills:\n"
    for i, u in enumerate(top_users, 1):
        text += f"{i}. User {u['user_id']} - {u['kills']} kills\n"
    await message.reply_text(text)
