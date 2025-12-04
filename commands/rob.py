from pyrogram import Client, filters
from database.db import get_user, update_user
import random

@app.on_message(filters.command("rob"))
async def rob(client, message):

    if not message.reply_to_message:
        return await message.reply("Reply to someone to rob!")

    thief = message.from_user
    target = message.reply_to_message.from_user

    thief_data = await get_user(thief.id)
    target_data = await get_user(target.id)

    if target_data["wallet"] < 100:
        return await message.reply("❌ Target has too little money to rob!")

    stolen = random.randint(50, target_data["wallet"])

    await update_user(thief.id, {"wallet": thief_data["wallet"] + stolen})
    await update_user(target.id, {"wallet": target_data["wallet"] - stolen})

    await message.reply(
        f"🔫 {thief.mention} robbed {target.mention} and stole **{stolen} coins!**"
    )
