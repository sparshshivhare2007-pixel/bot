import asyncio
import importlib

from NoxxNetwork import LOGGER, ChatBot  # NoxxBot -> ChatBot
from NoxxNetwork.modules import ALL_MODULES

async def anony_boot():
    try:
        await ChatBot.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)

    # Load all modules dynamically
    for all_module in ALL_MODULES:
        importlib.import_module("NoxxNetwork.modules." + all_module)

    LOGGER.info(f"@{ChatBot.username} Started.")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(anony_boot())
    LOGGER.info("Stopping NoxxNetwork Bot...")
