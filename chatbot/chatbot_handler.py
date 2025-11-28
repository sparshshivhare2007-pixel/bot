import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API"))

# Use latest working Google Model
MODEL_NAME = "gemini-1.5-flash"      # Fast, cheap & best for bot

async def chatbot_handler(update, context):

    # Do not respond to commands like /start /help
    if update.message.text.startswith("/"):
        return
    
    user_message = update.message.text

    try:
        model = genai.GenerativeModel(MODEL_NAME)

        # Generate response
        response = model.generate_content(user_message)

        bot_reply = response.text if response.text else "🙂"

        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text("⚠️ Chatbot Error: " + str(e))
