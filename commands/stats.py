from main import app
from pyrogram import filters
from database.db import users

@app.on_message(filters.command('stats') & filters.private)
async def stats_cmd(client, message):
    count = await users.count_documents({})
    await message.reply(f'Bot has {count} users in DB.')
