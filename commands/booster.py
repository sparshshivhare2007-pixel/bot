from main import app
from pyrogram import filters

@app.on_message(filters.command('booster') & filters.private)
async def booster_cmd(client, message):
    await message.reply('Booster stub. Add timed boosters to increase daily/work rewards.')
