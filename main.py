from pyrogram import Client
import config

app = Client(
    "RISHUCHATBOT",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# Import commands
from commands import balance, daily, rob, hug, topkill, couple

print("🤖 RISHUCHATBOT is running...")
app.run()
