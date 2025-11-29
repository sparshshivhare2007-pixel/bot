# Simple chatbot logic (can be replaced with AI/API later)
def get_chat_response(user_message: str) -> str:
    user_message = user_message.lower()
    
    if "hello" in user_message or "hi" in user_message:
        return "Hello! How are you?"
    elif "how are you" in user_message:
        return "I'm just a bot, but I'm doing great! 😄"
    else:
        return "Sorry, I didn't understand that. Ask me something else!"
