from pyrogram import filters
from pyrogram.types import Message
from main import app
import random

with open("data/couple_quotes.txt", "r") as f:
    quotes = [line.strip() for line in f.readlines()]

@app.on_message(filters.command("couple"))
async def couple(client, message: Message):
    quote = random.choice(quotes)
    await message.reply_text(f"💖 {quote}")
