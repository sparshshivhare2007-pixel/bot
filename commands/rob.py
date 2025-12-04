from main import app
from pyrogram import filters
from database.db import get_user, inc_user, users
import random

@app.on_message(filters.command('rob') & filters.group)
async def rob_cmd(client, message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply('Reply to a user to rob them.')
    thief = message.from_user
    target = message.reply_to_message.from_user
    if thief.id == target.id:
        return await message.reply("You can't rob yourself.")
    tdata = await get_user(target.id)
    if tdata.get('wallet',0) < 150:
        return await message.reply('Target has too little money.')
    # anti-grief: throttle robber via cooldown stored in user doc
    from database.db import upsert_user
    thief_doc = await get_user(thief.id)
    cd = thief_doc.get('cooldowns',{}).get('rob',0)
    import time
    now = int(time.time())
    if now - cd < 300:
        return await message.reply('You are on rob cooldown.')
    stolen = random.randint(50, min(400, tdata.get('wallet',0)))
    await users.update_one({'_id': thief.id}, {'$inc': {'wallet': stolen}, '$set': {'cooldowns.rob': now}}, upsert=True)
    await users.update_one({'_id': target.id}, {'$inc': {'wallet': -stolen}}, upsert=True)
    await message.reply(f"🔫 {thief.mention} robbed {target.mention} for {stolen} coins.")
