import asyncio
import importlib
from pyrogram import idle
from chatbot import LOGGER, ChatBot, ALL_MODULES  # ChatBot = your pyrogram client

async def bot_boot():
    try:
        await ChatBot.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)

    for module in ALL_MODULES:
        importlib.import_module(f"chatbot.modules.{module}")

    LOGGER.info(f"@{ChatBot.username} Started.")
    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(bot_boot())
    LOGGER.info("Stopping ChatBot...")
