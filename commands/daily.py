from pyrogram import filters
from pyrogram.types import Message
from helpers.users import get_user, update_user
from datetime import datetime, timedelta
from main import app

@app.on_message(filters.command("daily") & filters.group)
async def daily(client, message: Message):
    user = get_user(message.from_user.id)
    now = datetime.utcnow()

    if user["last_daily"] and now - user["last_daily"] < timedelta(hours=24):
        await message.reply_text("⏳ You already claimed daily reward!")
        return

    reward = 500
    user["balance"] += reward
    user["last_daily"] = now
    update_user(user["user_id"], user)
    await message.reply_text(f"🎁 You claimed {reward} coins!")
