import os
import importlib
from pyrogram import Client
import config

app = Client(
    "economy_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

# Import database early to create indices if needed
from database import db as _db

# Auto-load commands
commands_dir = os.path.join(os.path.dirname(__file__), "commands")
for filename in os.listdir(commands_dir):
    if filename.endswith(".py"):
        importlib.import_module(f"commands.{filename[:-3]}")

print("Starting Economy Bot...")
app.run()
