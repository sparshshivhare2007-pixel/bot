from main import app
from pyrogram import filters
from database.db import users
import random

@app.on_message(filters.command('lottery') & filters.private)
async def lottery_cmd(client, message):
    # stub: random small chance to win
    uid = message.from_user.id
    chance = random.randint(1,100)
    if chance == 1:
        amt = 5000
        await users.update_one({'_id': uid}, {'$inc': {'wallet': amt}}, upsert=True)
        await message.reply(f'🎉 Jackpot! You won {amt} coins.')
    else:
        await message.reply('No luck this time.')
