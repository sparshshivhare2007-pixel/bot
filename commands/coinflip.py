from main import app
from pyrogram import filters
import random

@app.on_message(filters.command('coinflip') & filters.private)
async def coinflip_cmd(client, message):
    args = message.text.split(maxsplit=1)
    choice = None
    if len(args) > 1:
        choice = args[1].strip().lower()
    res = random.choice(['heads','tails'])
    await message.reply(f'Result: {res}. You chose: {choice}')
