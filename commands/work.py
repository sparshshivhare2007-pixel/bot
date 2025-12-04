from main import app
from pyrogram import filters
from database.db import get_user, inc_user
import random
from pyrogram.types import Message

@app.on_message(filters.command('work') & filters.private)
async def work_cmd(client, message: Message):
    uid = message.from_user.id
    earn = random.randint(100, 450)
    await inc_user(uid, 'wallet', earn)
    await message.reply(f"👷 You worked and earned {earn} coins.", quote=True)
