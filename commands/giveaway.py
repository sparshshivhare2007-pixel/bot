from main import app
from pyrogram import filters

@app.on_message(filters.command('giveaway') & filters.private)
async def giveaway_cmd(client, message):
    await message.reply('Giveaway is a stub. Implement reaction-based giveaway if required.')
