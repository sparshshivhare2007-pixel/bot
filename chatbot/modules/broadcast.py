from pyrogram import filters
from chatbot.chatbot import ChatBot
from config import OWNER_ID

@ChatBot.on_message(filters.command("cbroadcast") & filters.user(OWNER_ID))
async def broadcast(bot, message):
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else None
    if not text:
        return await message.reply("Broadcast text do.")

    async for dialog in bot.get_dialogs():
        try:
            await bot.send_message(dialog.chat.id, text)
        except:
            pass

    await message.reply("Broadcast done!")
