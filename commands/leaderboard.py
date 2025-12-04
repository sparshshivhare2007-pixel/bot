from main import app
from pyrogram import filters
from pyrogram.types import Message
from database.db import users
import asyncio

@app.on_message(filters.command('leaderboard') & filters.private)
async def lb_cmd(client, message: Message):
    top = users.find().sort([('wallet', -1)]).limit(10)
    lines = []
    async for u in top:
        uid = u['_id']
        total = u.get('wallet',0) + u.get('bank',0)
        try:
            user = await client.get_users(uid)
            name = f"{user.first_name or ''} {getattr(user,'last_name', '')}".strip()
        except:
            name = str(uid)
        lines.append(f"{name}: {total}")
    if not lines:
        return await message.reply('No users yet.')
    await message.reply('\n'.join(lines))
