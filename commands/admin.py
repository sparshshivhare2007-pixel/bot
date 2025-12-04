from main import app
from pyrogram import filters
import config
from database.db import users
from pyrogram.types import Message

def is_admin(uid):
    return uid in getattr(config, 'ADMINS', [])

@app.on_message(filters.command('addbal') & filters.private)
async def addbal_cmd(client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply('Admin only.')
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        return await message.reply('Usage: /addbal <user_id> <amount>')
    try:
        target = int(args[1]); amt = int(args[2])
    except:
        return await message.reply('Invalid args.')
    await users.update_one({'_id': target}, {'$inc': {'wallet': amt}}, upsert=True)
    await message.reply(f'Added {amt} to {target}.')

@app.on_message(filters.command('resetuser') & filters.private)
async def resetuser_cmd(client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply('Admin only.')
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply('Usage: /resetuser <user_id>')
    try:
        target = int(args[1])
    except:
        return await message.reply('Invalid id.')
    await users.delete_one({'_id': target})
    await message.reply(f'Reset user {target}.')
