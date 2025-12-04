from pyrogram import filters
from pyrogram.types import Message
from helpers.users import get_user, update_user
from helpers.utils import random_reward
from main import app
import random

@app.on_message(filters.command("rob"))
async def rob(client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Reply to someone to rob them!")
        return

    target_id = message.reply_to_message.from_user.id
    if target_id == message.from_user.id:
        await message.reply_text("You cannot rob yourself!")
        return

    thief = get_user(message.from_user.id)
    victim = get_user(target_id)

    success = random.choice([True, False])
    if success:
        amount = min(victim["balance"], random_reward(50, 200_
