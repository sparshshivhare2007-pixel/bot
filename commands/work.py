from main import app
from pyrogram import filters
from pyrogram.types import Message
from database.db import get_user, add_wallet
import random

@app.on_message(filters.command("work") & filters.private)
async def work_cmd(client, message: Message):
    uid = message.from_user.id
    earned = random.randint(50, 300)
    await add_wallet(uid, earned)
    await message.reply(f"👷 You worked and earned {earned} coins.", quote=True)
