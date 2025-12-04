from pyrogram import Client, filters
import config

# Create Pyrogram client
app = Client(
    "RISHUCHATBOT",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# Import command functions
from commands.balance import balance
from commands.daily import daily
from commands.rob import rob
from commands.hug import hug
from commands.topkill import topkill
from commands.couple import couple

# Register handlers
app.add_handler(filters.command("balance") & filters.private, balance)
app.add_handler(filters.command("daily") & filters.private, daily)
app.add_handler(filters.command("rob") & filters.group, rob)       # assuming rob is group-only
app.add_handler(filters.command("hug") & filters.private, hug)
app.add_handler(filters.command("topkill") & filters.group, topkill)
app.add_handler(filters.command("couple") & filters.private, couple)

print("🤖 RISHUCHATBOT is running...")
app.run()
