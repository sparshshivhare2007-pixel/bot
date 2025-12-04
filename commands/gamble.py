from main import app
from pyrogram import filters
from database.db import get_user, users
import random, re

@app.on_message(filters.command('gamble') & filters.private)
async def gamble_cmd(client, message):
    args = message.text.split(maxsplit=1)
    if len(args)<2:
        return await message.reply('Usage: /gamble <amount>')
    try:
        amt = int(re.sub('[^0-9]','', args[1]))
    except:
        return await message.reply('Invalid amount.')
    uid = message.from_user.id
    user = await get_user(uid)
    if user.get('wallet',0) < amt:
        return await message.reply('Not enough money.')
    # simple 50/50 double or lose
    win = random.choice([True, False])
    if win:
        await users.update_one({'_id': uid}, {'$inc': {'wallet': amt}}, upsert=True)
        return await message.reply(f'You won {amt}!')
    else:
        await users.update_one({'_id': uid}, {'$inc': {'wallet': -amt}}, upsert=True)
        return await message.reply(f'You lost {amt}.')
