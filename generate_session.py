"""
Run this ONCE, locally, on your own machine.
It logs into your Telegram account interactively (phone number + code)
and prints a session string. Copy that string into a GitHub secret
called TG_SESSION. Never commit it to the repo.

pip install telethon --break-system-packages   (or in a venv)
"""

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()
api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("\nLogged in. Your session string (save this as the TG_SESSION secret):\n")
    print(client.session.save())
