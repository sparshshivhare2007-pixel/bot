from main import app
from pyrogram import filters
from database.db import get_user, users

@app.on_message(filters.command('marry') & filters.private)
async def marry_cmd(client, message):
    # marry by reply
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply('Reply to user to propose.')
    uid = message.from_user.id
    target = message.reply_to_message.from_user
    if uid == target.id:
        return await message.reply('You cannot marry yourself.')
    # set married for both (no checks)
    await users.update_one({'_id': uid}, {'$set': {'married': target.id}}, upsert=True)
    await users.update_one({'_id': target.id}, {'$set': {'married': uid}}, upsert=True)
    await message.reply(f'💍 {message.from_user.mention} married {target.mention}!')
