from chatbot.gemini_client import ask_gemini

async def chatbot_handler(update, context):
    user_text = update.message.text

    # AI Response
    reply = await ask_gemini(user_text)

    await update.message.reply_text(reply)
