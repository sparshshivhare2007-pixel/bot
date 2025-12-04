from main import app
from pyrogram import filters

@app.on_message(filters.command('trivia') & filters.private)
async def trivia_cmd(client, message):
    # stub: you can integrate an API later
    await message.reply('Trivia is a stub — integrate an API or add Q/A here.')
