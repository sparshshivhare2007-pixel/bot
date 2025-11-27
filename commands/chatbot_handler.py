import httpx
import os
import asyncio
from telegram import Update
from telegram.ext import CallbackContext

# Gemini API configuration
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
# Ensure your Gemini API Key is set in your .env file as GEMINI_API_KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

async def generate_response(prompt: str) -> str:
    """Makes a call to the Gemini API to generate content with exponential backoff."""
    if not GEMINI_API_KEY:
        return "❌ Gemini API Key not found. Please set the GEMINI_API_KEY environment variable in your .env file."

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
    }

    # Basic exponential backoff logic for retries
    MAX_RETRIES = 3
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                    json=payload
                )
                response.raise_for_status() 
                
                # Process the response
                data = response.json()
                text = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Could not generate a response.')
                return text

        except httpx.HTTPStatusError as e:
            if e.response.status_code in (429, 503) and attempt < MAX_RETRIES - 1:
                delay = 2 ** attempt
                # Note: In a real environment, you might log this.
                await asyncio.sleep(delay)
            else:
                return "Sorry, I ran into a server error while thinking."
        except Exception:
            return "Sorry, I ran into an unexpected error."
            
    return "The API failed after several retries."


async def chatbot_handler(update: Update, context: CallbackContext):
    """
    Handles all non-command text messages. 
    In groups, responds only if the bot is mentioned. In DMs, responds to all text.
    """
    
    full_text = update.message.text
    bot_username = context.bot.username
    prompt = ""

    # Group Chat Logic: Respond only if mentioned
    if update.effective_chat.type in ["group", "supergroup"]:
        mention_tag = f"@{bot_username}"
        
        # Check if the message starts with a mention or is a reply to the bot
        if full_text and full_text.startswith(mention_tag):
            prompt = full_text[len(mention_tag):].strip()
        elif update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
            # If it's a reply to the bot
            prompt = full_text
        else:
            # Ignore messages not directed at the bot in groups
            return
            
    # Private Chat Logic: Respond to all messages
    elif update.effective_chat.type == "private":
        prompt = full_text

    if not prompt:
        return # Ignore empty prompts or only mentions

    # Show typing status while waiting for API
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Generate response
    response_text = await generate_response(prompt)
    
    # Reply to the user
    await update.message.reply_text(response_text)
