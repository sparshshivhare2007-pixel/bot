from pyrogram import Client, filters
from database.db import get_user

@app.on_message(filters.command("balance"))
async def balance_cmd(client, message):
    user = await get_user(message.from_user.id)

    await message.reply(
        f"**💰 Your Balance**\n\n"
        f"👛 Wallet: `{user['wallet']}`\n"
        f"🏦 Bank: `{user['bank']}`"
    )
