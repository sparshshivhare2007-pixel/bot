from main import app
from pyrogram import filters
from pyrogram.types import Message
from database.db import get_user, inc_user
import time

DAILY = 700

@app.on_message(filters.command('daily') & filters.private)
async def daily_cmd(client, message: Message):
    uid = message.from_user.id
    user = await get_user(uid)
    now = int(time.time())
    if now - user.get('daily',0) < 86400:
        rem = 86400 - (now - user.get('daily',0))
        h = rem//3600
        m = (rem%3600)//60
        return await message.reply(f"⏳ Daily available in {h}h {m}m", quote=True)
    await inc_user(uid, 'wallet', DAILY)
    await upsert_daily(uid, now)
    await message.reply(f"🎉 You claimed {DAILY} coins!", quote=True)

# helper to set daily
from database.db import upsert_user
async def upsert_daily(uid, now):
    user = await get_user(uid)
    user['daily'] = now
    await upsert_user(uid, user)
