from main import app
from pyrogram import filters
from database.db import get_user, users
import re

@app.on_message(filters.command('gift') & filters.private)
async def gift_cmd(client, message):
    # usage: /gift <reply or id> <amount>
    args = message.text.split(maxsplit=2)
    if len(args) < 3 and not message.reply_to_message:
        return await message.reply('Usage: /gift <user_id|reply> <amount>')
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user.id
        amt = int(re.sub('[^0-9]','', args[1]))
    else:
        target = int(args[1])
        amt = int(re.sub('[^0-9]','', args[2]))
    uid = message.from_user.id
    user = await get_user(uid)
    if user.get('wallet',0) < amt:
        return await message.reply('Not enough money.')
    await users.update_one({'_id': uid}, {'$inc': {'wallet': -amt}})
    await users.update_one({'_id': target}, {'$inc': {'wallet': amt}}, upsert=True)
    await message.reply(f'Gifted {amt} to {target}.')
