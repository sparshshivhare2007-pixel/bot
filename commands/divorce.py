from main import app
from pyrogram import filters
from database.db import get_user, users

@app.on_message(filters.command('divorce') & filters.private)
async def divorce_cmd(client, message):
    uid = message.from_user.id
    user = await get_user(uid)
    partner = user.get('married')
    if not partner:
        return await message.reply('You are not married.')
    await users.update_one({'_id': uid}, {'$set': {'married': None}}, upsert=True)
    await users.update_one({'_id': partner}, {'$set': {'married': None}}, upsert=True)
    await message.reply('You are now divorced.')
