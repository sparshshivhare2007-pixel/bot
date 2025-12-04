from main import app
from pyrogram import filters
from database.db import get_user

@app.on_message(filters.command('profile') & filters.private)
async def profile_cmd(client, message):
    uid = message.from_user.id
    user = await get_user(uid)
    total = user.get('wallet',0) + user.get('bank',0)
    married = user.get('married')
    await message.reply(f"User: {message.from_user.mention}\nTotal balance: {total}\nMarried to: {married}", quote=True)
