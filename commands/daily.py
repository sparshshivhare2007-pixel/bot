from pyrogram import Client, filters
from database.db import get_user, update_user
from time import time

DAILY_REWARD = 500

@app.on_message(filters.command("daily"))
async def daily(client, message):
    uid = message.from_user.id
    user = await get_user(uid)

    now = int(time())
    
    if now - user["daily"] < 86400:
        remaining = 86400 - (now - user["daily"])
        hours = remaining // 3600
        return await message.reply(f"⏳ Daily reward is available in {hours} hours.")

    await update_user(uid, {
        "wallet": user["wallet"] + DAILY_REWARD,
        "daily": now
    })

    await message.reply(f"🎉 You received **{DAILY_REWARD} coins!**")
