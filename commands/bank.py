from main import app
from pyrogram import filters
from pyrogram.types import Message
from database.db import get_user, users
import re

@app.on_message(filters.command("deposit") & filters.private)
async def deposit_cmd(client, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("Usage: /deposit <amount>")
    try:
        amt = int(re.sub(r'[^0-9]','', args[1]))
    except:
        return await message.reply("Invalid amount.")
    uid = message.from_user.id
    user = await get_user(uid)
    if user.get('wallet',0) < amt:
        return await message.reply('Not enough in wallet.')
    await users.update_one({'_id': uid}, {'$inc': {'wallet': -amt, 'bank': amt}})
    await message.reply(f'Deposited {amt} coins.')

@app.on_message(filters.command("withdraw") & filters.private)
async def withdraw_cmd(client, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("Usage: /withdraw <amount>")
    try:
        amt = int(re.sub(r'[^0-9]','', args[1]))
    except:
        return await message.reply("Invalid amount.")
    uid = message.from_user.id
    user = await get_user(uid)
    if user.get('bank',0) < amt:
        return await message.reply('Not enough in bank.')
    await users.update_one({'_id': uid}, {'$inc': {'bank': -amt, 'wallet': amt}})
    await message.reply(f'Withdrew {amt} coins.')
