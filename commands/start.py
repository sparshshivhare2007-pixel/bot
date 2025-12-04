from main import app
from pyrogram import filters
from pyrogram.types import Message

@app.on_message(filters.command('start') & filters.private)
async def start_cmd(client, message: Message):
    await message.reply('👋 Welcome! Use /help to see economy commands.')
