import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API"))

# Gemini v1 API clients
client = genai.GenerativeModel("gemini-1.5-flash")

async def chatbot_handler(update, context):

    if update.message.text.startswith("/"):
        return

    user_message = update.message.text

    try:
        response = client.generate_content(
            contents=user_message
        )

        bot_reply = response.text or "🙂"

        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text("⚠️ Chatbot Error: " + str(e))
