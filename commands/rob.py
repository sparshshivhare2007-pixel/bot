from main import app
from pyrogram import filters
from pyrogram.types import Message
from database.db import get_user, add_wallet, users
import random

@app.on_message(filters.command("rob") & filters.group)
async def rob_cmd(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply("Reply to a user to rob them.")
    thief = message.from_user
    target = message.reply_to_message.from_user
    if thief.id == target.id:
        return await message.reply("You can't rob yourself.")
    tdata = await get_user(target.id)
    if tdata.get("wallet",0) < 100:
        return await message.reply("Target has too little money to be worth robbing.")
    stolen = random.randint(50, min(500, tdata.get("wallet",0)))
    # update thief and target
    await users.update_one({"_id": thief.id}, {"$inc": {"wallet": stolen}}, upsert=True)
    await users.update_one({"_id": target.id}, {"$inc": {"wallet": -stolen}}, upsert=True)
    await message.reply(f"🔫 {thief.mention} robbed {target.mention} for {stolen} coins.")
