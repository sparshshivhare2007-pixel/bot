#!/bin/bash

echo "🚀 Starting Economy Bot..."
python3 economy/main.py &

echo "🤖 Starting ChatBot..."
python3 chatbot/main.py &

wait
