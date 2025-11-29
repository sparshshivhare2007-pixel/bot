from .start import chatbot_start
from .chat_ai import ai_chat
from .ping import ping
from .stats import stats

def setup_chatbot_handlers(app):
    app.add_handler(CommandHandler("cstart", chatbot_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))
    app.add_handler(CommandHandler("cping", ping))
    app.add_handler(CommandHandler("cstats", stats))
