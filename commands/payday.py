from main import app
from pyrogram import filters
from database.db import users
import random

@app.on_message(filters.command('payday') & filters.private)
async def payday_cmd(client, message):
    # stub: give small passive income
    uid = message.from_user.id
    amt = random.randint(10,100)
    await users.update_one({'_id': uid}, {'$inc': {'wallet': amt}}, upsert=True)
    await message.reply(f'Payday: you received {amt} coins.')
