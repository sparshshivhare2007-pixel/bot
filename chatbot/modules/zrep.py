import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from chatbot import ChatBot
from config import IMG

start_txt = "<b>Welcome to ChatBot!</b>"

repo_buttons = [
    [InlineKeyboardButton("Music Bot", url="http://github.com/...")],
    [InlineKeyboardButton("ChatBot", url="http://github.com/...")]
]

@ChatBot.on_message(filters.command(["repo", "repos", "source"]))
async def repo_handler(_, message):
    await message.reply_photo(photo=random.choice(IMG), caption=start_txt, reply_markup=InlineKeyboardMarkup(repo_buttons))
