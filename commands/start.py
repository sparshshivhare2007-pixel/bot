from main import app
from pyrogram import filters
from pyrogram.types import Message

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    await message.reply(
        "👋 Welcome to the Economy Bot!\n"
        "Use /balance to check money, /daily for daily reward, /work to earn, /rob to rob (reply), /leaderboard to view top users."
    )
