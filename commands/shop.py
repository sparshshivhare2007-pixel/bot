from main import app
from pyrogram import filters
from database.db import items
from pyrogram.types import Message

@app.on_message(filters.command('shop') & filters.private)
async def shop_cmd(client, message: Message):
    cur = items.find()
    lines = []
    async for it in cur:
        lines.append(f"{it['name']} - {it['price']}\n{it.get('desc','')}")
    if not lines:
        return await message.reply('Shop is empty.')
    await message.reply('\n\n'.join(lines), quote=True)
