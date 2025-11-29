from chatbot.chatbot import ChatBot
from chatbot.modules import *
import asyncio

async def start_chatbot():
    await ChatBot.start()
    print("🤖 Chatbot started!")
    await asyncio.Event().wait()
