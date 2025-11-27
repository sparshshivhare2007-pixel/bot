import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API"))

async def chatbot_handler(update, context):

    # ✅ FIX: Do not respond to commands
    if update.message.text.startswith("/"):
        return

    user_message = update.message.text

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_message)

        bot_reply = response.text
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text("⚠️ Chatbot Error: " + str(e))
