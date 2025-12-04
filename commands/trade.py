from main import app
from pyrogram import filters

@app.on_message(filters.command('trade') & filters.private)
async def trade_cmd(client, message):
    await message.reply('Trade is a stub. Implement offer/accept logic if needed.')
