from main import app
from pyrogram import filters
from database.db import inc_user
import random

@app.on_message(filters.command('beg') & filters.private)
async def beg_cmd(client, message):
    uid = message.from_user.id
    amt = random.randint(10, 200)
    await inc_user(uid, 'wallet', amt)
    await message.reply(f"🙏 Someone gave you {amt} coins.", quote=True)
