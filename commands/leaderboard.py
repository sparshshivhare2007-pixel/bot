from main import app
from pyrogram import filters
from database.db import users
from pyrogram.types import Message

@app.on_message(filters.command('leaderboard') & filters.private)
async def lb_cmd(client, message: Message):
    cur = users.find().sort([('wallet', -1)]).limit(10)
    lines = []
    async for u in cur:
        uid = u['_id']
        total = u.get('wallet',0) + u.get('bank',0)
        try:
            user = await client.get_users(uid)
            name = user.first_name or str(uid)
        except:
            name = str(uid)
        lines.append(f"{name}: {total}")
    if not lines:
        return await message.reply('No users yet.')
    await message.reply('\n'.join(lines))
