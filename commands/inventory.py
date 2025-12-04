from main import app
from pyrogram import filters
from database.db import get_user

@app.on_message(filters.command('inventory') & filters.private)
async def inv_cmd(client, message):
    uid = message.from_user.id
    user = await get_user(uid)
    inv = user.get('inventory',[])
    if not inv:
        return await message.reply('Inventory is empty.')
    lines = [f"- {i.get('name')} : {i.get('desc','')}" for i in inv]
    await message.reply('\n'.join(lines), quote=True)
