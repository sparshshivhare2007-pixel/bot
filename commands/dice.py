from main import app
from pyrogram import filters
import random

@app.on_message(filters.command('dice') & filters.private)
async def dice_cmd(client, message):
    val = random.randint(1,6)
    await message.reply(f'🎲 You rolled {val}')
