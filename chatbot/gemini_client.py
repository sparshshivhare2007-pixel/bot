import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API"))

client = genai.GenerativeModel("gemini-1.5-flash")

async def ask_gemini(text):
    try:
        response = client.generate_content(contents=text)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"
