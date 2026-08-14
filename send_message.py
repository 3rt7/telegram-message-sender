"""
Runs inside GitHub Actions on a schedule.
Sends either two fixed emojis, or a Groq-generated one-liner, to one person.

Reads everything from environment variables (set as GitHub Actions secrets):
  TG_API_ID, TG_API_HASH, TG_SESSION, TG_RECIPIENT, GROQ_API_KEY (optional)
"""

import os
import random
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ.get("TG_API_ID"))
API_HASH = os.environ.get("TG_API_HASH")
SESSION = os.environ.get("TG_SESSION")
RECIPIENT = os.environ.get("TG_RECIPIENT")  # username like "@someone" or numeric user id
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # leave unset to just send emojis

EMOJIS = ["❤️", "😘", "😠", "🍆"]


def get_message():
    if not GROQ_API_KEY:
        return " ".join(random.sample(EMOJIS, 1))

#    import urllib.request
#    import json
#
#    payload = {
#        "model": "llama-3.3-70b-versatile",
#        "messages": [
#            {
#                "role": "user",
#                "content": (
#                    "Send one short, casual, random message to a friend. "
#                    "Under 10 words. No explanation, just the message itself."
#                ),
#            }
#        ],
#        "max_tokens": 30,
#    }
#
#    req = urllib.request.Request(
#        "https://api.groq.com/openai/v1/chat/completions",
#        data=json.dumps(payload).encode(),
#        headers={
#            "Authorization": f"Bearer {GROQ_API_KEY}",
#            "Content-Type": "application/json",
#        },
#    )
#
#    try:
#        with urllib.request.urlopen(req, timeout=15) as resp:
#            data = json.loads(resp.read())
#            return data["choices"][0]["message"]["content"].strip()
#    except Exception as e:
#        print(f"Groq call failed, falling back to emojis: {e}")
#        return " ".join(random.sample(EMOJIS, 1))


def main():
    message = get_message()
    with TelegramClient(StringSession(SESSION), API_ID, API_HASH) as client:
        client.send_message(RECIPIENT, message)
    print(f"Sent: {message}")


if __name__ == "__main__":
    main()
