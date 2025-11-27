# bot.py
import os
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

# ----------------- Import commands -----------------
from commands.start import start
from commands.balance import balance
from commands.work import work
from commands.daily import daily
from commands.rob import rob
from commands.protect import protect
from commands.toprich import toprich
from commands.topkill import topkill
from commands.kill import kill
from commands.revive import revive
from commands.close import close
from commands.open import open_economy
from commands.claim import claim
from commands.own import own
from commands.couple import couple
from commands.crush import crush
from commands.love import love
from commands.slap import slap
from commands.items import items
from commands.item import item
from commands.give import give

# ----------------- Add handlers -----------------
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("work", work))
app.add_handler(CommandHandler("daily", daily))
app.add_handler(CommandHandler("rob", rob))
app.add_handler(CommandHandler("protect", protect))
app.add_handler(CommandHandler("toprich", toprich))
app.add_handler(CommandHandler("topkill", topkill))
app.add_handler(CommandHandler("kill", kill))
app.add_handler(CommandHandler("revive", revive))
app.add_handler(CommandHandler("close", close))
app.add_handler(CommandHandler("open", open_economy))
app.add_handler(CommandHandler("claim", claim))
app.add_handler(CommandHandler("own", own))
app.add_handler(CommandHandler("couple", couple))
app.add_handler(CommandHandler("crush", crush))
app.add_handler(CommandHandler("love", love))
app.add_handler(CommandHandler("slap", slap))
app.add_handler(CommandHandler("items", items))
app.add_handler(CommandHandler("item", item))
app.add_handler(CommandHandler("give", give))

if __name__ == "__main__":
    app.run_polling()
