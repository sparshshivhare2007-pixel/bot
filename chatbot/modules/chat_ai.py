from pyrogram import filters
from chatbot.chatbot import ChatBot
import random

RESPONSES = [
    "Aur batao 😄",
    "Hmm, interesting! 😁",
    "Nicee 🔥",
    "Bhot sahi 😎",
    "I'm here ❤️",
]

@ChatBot.on_message(filters.private & ~filters.command(["start", "help", "broadcast"]))
async def auto_chat(bot, message):
    await message.reply_text(random.choice(RESPONSES))
