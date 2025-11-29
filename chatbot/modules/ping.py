import random
from datetime import datetime
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup
from chatbot import ChatBot
from chatbot.database.chats import add_served_chat
from chatbot.database.users import add_served_user
from config import IMG, STICKER, OWNER_USERNAME

@ChatBot.on_message(filters.command("ping"))
async def ping(_, message):
    await message.reply_sticker(sticker=random.choice(STICKER))
    start = datetime.now()
    loda = await message.reply_photo(photo=random.choice(IMG), caption="ᴘɪɴɢɪɴɢ...")
    ms = (datetime.now() - start).microseconds / 1000
    await loda.edit_text(f"Bot alive! Ping: `{ms}` ms", reply_markup=InlineKeyboardMarkup([]))
    if message.chat.type == ChatType.PRIVATE:
        await add_served_user(message.from_user.id)
    else:
        await add_served_chat(message.chat.id)
