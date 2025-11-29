# main.py (bottom me ya jahaan handlers register ho rahe hain)

from chat.commands import chat_reply  # aapke chatbot me message handler function

# Chatbot handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_reply))
