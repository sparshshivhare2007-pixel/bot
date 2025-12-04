from main import app
from pyrogram import filters
from pyrogram.types import Message
from database.db import get_user, add_wallet
import time

DAILY = 500

@app.on_message(filters.command("daily") & filters.private)
async def daily_cmd(client, message: Message):
    uid = message.from_user.id
    user = await get_user(uid)
    now = int(time.time())
    if now - user.get("daily",0) < 86400:
        remaining = 86400 - (now - user.get("daily",0))
        hours = remaining // 3600
        mins = (remaining % 3600) // 60
        return await message.reply(f"⏳ Daily available in {hours}h {mins}m", quote=True)
    await add_wallet(uid, DAILY)
    from database.db import users
    await users.update_one({"_id": uid}, {"$set": {"daily": now}}, upsert=True)
    await message.reply(f"🎉 You received {DAILY} coins!", quote=True)
