from main import app
from pyrogram import filters
from database.db import get_user, users
import re

@app.on_message(filters.command('transfer') & filters.private)
async def transfer_cmd(client, message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        return await message.reply('Usage: /transfer <user_id|reply> <amount>')
    target_raw = args[1]
    amt_raw = args[2]
    try:
        amt = int(re.sub('[^0-9]','', amt_raw))
    except:
        return await message.reply('Invalid amount.')
    uid = message.from_user.id
    user = await get_user(uid)
    if user.get('wallet',0) < amt:
        return await message.reply('Not enough money.')
    # support reply or id
    if message.reply_to_message and message.reply_to_message.from_user:
        target_id = message.reply_to_message.from_user.id
    else:
        try:
            target_id = int(target_raw)
        except:
            return await message.reply('Invalid target.')
    await users.update_one({'_id': uid}, {'$inc': {'wallet': -amt}})
    await users.update_one({'_id': target_id}, {'$inc': {'wallet': amt}}, upsert=True)
    await message.reply(f'Transferred {amt} to {target_id}.')
