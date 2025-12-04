@app.on_message(filters.command("balance") & filters.private)
async def balance(client: Client, message: Message):
    user = get_user(message.from_user.id)
    balance = user.get("balance", 0)
    await message.reply_text(f"💰 Your balance: ${balance}")
