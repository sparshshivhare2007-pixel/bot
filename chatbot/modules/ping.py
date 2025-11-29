import random
from datetime import datetime
from telegram import InlineKeyboardMarkup, ChatType
from helpers import add_served_user, add_served_chat

# Your stickers and images
STICKER = [
    "CAACAgUAAxkBAAEJ2VllrQYl",
    "CAACAgUAAxkBAAEJ2VllrQT6",
    "CAACAgUAAxkBAAEJ2VllrQKf",
]

IMG = [
    "https://files.catbox.moe/abcd1.jpg",
    "https://files.catbox.moe/abcd2.jpg",
    "https://files.catbox.moe/abcd3.jpg",
]


async def ping(update, context):
    message = update.message

    # Reply sticker
    await message.reply_sticker(sticker=random.choice(STICKER))

    # Start time
    start = datetime.now()

    # Reply image + caption
    loading = await message.reply_photo(
        photo=random.choice(IMG),
        caption="ᴘɪɴɢɪɴɢ..."
    )

    # Time taken (ms)
    ms = (datetime.now() - start).microseconds / 1000

    # Edit message with final ping result
    await loading.edit_caption(
        caption=f"Bot alive! Ping: `{ms}` ms",
        reply_markup=InlineKeyboardMarkup([])
    )

    # Save served user/chat
    if message.chat.type == ChatType.PRIVATE:
        await add_served_user(message.from_user.id)
    else:
        await add_served_chat(message.chat.id)
