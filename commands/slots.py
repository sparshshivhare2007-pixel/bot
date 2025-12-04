from main import app
from pyrogram import filters
import random

@app.on_message(filters.command('slots') & filters.private)
async def slots_cmd(client, message):
    reels = [random.choice(['🍒','🍋','🔔','7']) for _ in range(3)]
    text = ' | '.join(reels)
    win = len(set(reels)) == 1
    await message.reply(f"{text}\nWin: {win}")
