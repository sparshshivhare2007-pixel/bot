from main import app
from pyrogram import filters
from database.db import users

@app.on_message(filters.command('leaderboard_group') & filters.group)
async def lb_group(client, message):
    # simple group leaderboard by wallet
    cur = users.find().sort([('wallet', -1)]).limit(10)
    lines = []
    async for u in cur:
        lines.append(f"{u.get('_id')}: {u.get('wallet',0)}")
    if not lines:
        return await message.reply('No users yet.')
    await message.reply('\n'.join(lines))
