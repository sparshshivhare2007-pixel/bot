from main import app
from pyrogram import filters
from pyrogram.types import Message
from database.db import get_user

@app.on_message(filters.command("balance") & filters.private)
async def balance_cmd(client, message: Message):
    uid = message.from_user.id
    user = await get_user(uid)
    await message.reply(
        f"💰 Balance:\nWallet: `{user.get('wallet',0)}`\nBank: `{user.get('bank',0)}`",
        quote=True
    )
