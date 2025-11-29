import asyncio
import random
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup
from chatbot import ChatBot
from chatbot.database.chats import add_served_chat
from chatbot.database.users import add_served_user
from config import IMG, STICKER, DEV_OP, START, HELP_BTN

@ChatBot.on_message(filters.command(["start", "aistart"]))
async def start(_, message):
    if message.chat.type == ChatType.PRIVATE:
        accha = await message.reply_text(random.choice(["Starting..."]))
        await asyncio.sleep(1)
        await accha.delete()
        await message.reply_sticker(sticker=random.choice(STICKER))
        await message.reply_photo(photo=random.choice(IMG), caption=f"Hi, I am ChatBot", reply_markup=InlineKeyboardMarkup(DEV_OP))
        await add_served_user(message.from_user.id)
    else:
        await message.reply_photo(photo=random.choice(IMG), caption=START, reply_markup=InlineKeyboardMarkup(DEV_OP))
        await add_served_chat(message.chat.id)
