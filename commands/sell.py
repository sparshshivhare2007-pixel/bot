from main import app
from pyrogram import filters
from database.db import get_user, remove_item, users
import re

@app.on_message(filters.command('sell') & filters.private)
async def sell_cmd(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply('Usage: /sell <item name>')
    name = args[1].strip()
    uid = message.from_user.id
    user = await get_user(uid)
    inv = user.get('inventory',[])
    found = None
    for it in inv:
        if it.get('name','').lower() == name.lower():
            found = it
            break
    if not found:
        return await message.reply('You do not have that item.')
    # simple sell: price = half of assumed price (if known)
    price = 100
    await remove_item(uid, found.get('name'))
    await users.update_one({'_id': uid}, {'$inc': {'wallet': price}}, upsert=True)
    await message.reply(f'Sold {found.get("name")} for {price} coins.')
