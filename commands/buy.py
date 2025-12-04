from main import app
from pyrogram import filters
from database.db import items, users, add_item, get_user
import re

@app.on_message(filters.command('buy') & filters.private)
async def buy_cmd(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply('Usage: /buy <item name>')
    name = args[1].strip()
    it = await items.find_one({'name':{'$regex':f'^{name}$', '$options':'i'}})
    if not it:
        return await message.reply('Item not found.')
    uid = message.from_user.id
    user = await get_user(uid)
    if user.get('wallet',0) < it['price']:
        return await message.reply('Not enough money.')
    await users.update_one({'_id': uid}, {'$inc': {'wallet': -it['price']}})
    await add_item(uid, {'name': it['name'], 'desc': it.get('desc','')})
    await message.reply(f'You bought {it['name']} for {it['price']} coins.')
