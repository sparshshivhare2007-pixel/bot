from main import app
from pyrogram import filters
from pyrogram.types import Message
from database.db import get_user, add_wallet
import random

@app.on_message(filters.command("beg") & filters.private)
async def beg_cmd(client, message: Message):
    uid = message.from_user.id
    amt = random.randint(10, 150)
    await add_wallet(uid, amt)
    await message.reply(f"🙏 Someone gave you {amt} coins.", quote=True)
