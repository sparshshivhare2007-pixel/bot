from pyrogram import filters
from pyrogram.enums import ParseMode
from chatbot import ChatBot

@ChatBot.on_message(filters.command("id"))
async def get_id(client, message):
    reply = message.reply_to_message
    text = f"✨ <b>ID Information</b>\n\n"
    text += f"📩 Message ID: {message.id}\n"
    text += f"🙋 Your ID: {message.from_user.id}\n"
    text += f"💬 Chat ID: {message.chat.id}\n\n"
    if reply and reply.from_user:
        text += f"🔁 Replied Msg ID: {reply.id}\n"
        text += f"👤 Replied User ID: {reply.from_user.id}\n"
    await message.reply_text(text, disable_web_page_preview=True, parse_mode=ParseMode.HTML)
