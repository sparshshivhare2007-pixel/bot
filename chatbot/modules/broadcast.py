import asyncio
from pyrogram import filters
from pyrogram.types import Message
from chatbot import ChatBot
from chatbot.helpers import add_served_chat, add_served_user, get_served_chats, get_served_users
from config import OWNER_ID

@ChatBot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(_, message: Message):
    reply = message.reply_to_message
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    if not reply and not text:
        return await message.reply_text("❖ Reply to a message or provide text to broadcast.")

    progress_msg = await message.reply_text("❖ Broadcasting message... Please wait")
    sent_groups, sent_users, failed, pinned = 0, 0, 0, 0

    chats_data = await get_served_chats()
    users_data = await get_served_users()

    recipients = []

    if text:
        # Broadcast text to all
        recipients = chats_data + users_data
    elif reply:
        # Broadcast replied message
        recipients = chats_data + users_data

    for r in recipients:
        try:
            await _.send_message(r, text or reply.text)
            if r in chats_data:
                sent_groups += 1
            else:
                sent_users += 1
            await asyncio.sleep(0.3)
        except Exception:
            failed += 1

    await progress_msg.edit_text(
        f"✅ Broadcast Completed\n"
        f"Groups: {sent_groups}\nUsers: {sent_users}\nFailed: {failed}"
    )
