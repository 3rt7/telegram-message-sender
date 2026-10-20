"""
Runs inside GitHub Actions.

Short runs are scheduled from 08:30 through 19:30 UTC. A hash of the UTC date
picks one of them; that run sends one random line from TEXTS plus one random
emoji from EMOJIS. Every other run exits immediately.

The cron strings in SLOTS must match .github/workflows/daily-message.yml.
GitHub passes the triggering cron as SLOT. workflow_dispatch sets FORCE_SEND
and sends immediately, which is also what a local `python send_message.py` does.

Secrets, set as environment variables: TG_API_ID, TG_API_HASH, TG_SESSION, TG_RECIPIENT.
"""

import hashlib
import os
import random
import sys
from datetime import datetime, timezone

TEXTS = [
    "دلم برات تنگ شد",
    "بهت فکر کردم",
    "دوست دارم",
    "همش میای تو ذهنم",
    "روزت خیلی خوب باشهههه",
    "امیدوارم به زودی ببینمت",
    "خیلی خوشحالم که دارمت",
    "سلام علیکم",
    "سلام بابایی",
    "بیا بغل بابا",
    "الان میخوامت",
    "خیلی بهت فکر میکنم",
    "جیگگگرتووووو",
    "جیگرتو میدی بخورم؟",
    "بابایی خوش ذوق خودم"
]

EMOJIS = [
    "❤️❤️",
    "😘",
    "😈",
    "🍆",
    "💦",
    "😉",
    "🥲",
    "🫵🏽😄",
    "🐿️",
    "🍑",
    "🌶️",
    "🍓",
    "🍫",
]

# Minute 0 is omitted. GitHub often delays or drops jobs at the top of the hour.
# One hash of the UTC date picks a single entry from this list.
SLOTS = [
    "30 6 * * *",
    "5 7 * * *",
    "30 7 * * *",
    "5 8 * * *",
    "30 8 * * *",
    "5 9 * * *",
    "30 9 * * *",
    "5 10 * * *",
    "30 10 * * *",
    "5 11 * * *",
    "30 11 * * *",
    "5 12 * * *",
    "30 12 * * *",
    "5 13 * * *",
    "30 13 * * *",
    "30 14 * * *",
    "5 15 * * *",
    "30 15 * * *",
    "5 16 * * *",
    "30 16 * * *",
    "5 17 * * *",
    "30 17 * * *",
    "5 18 * * *",
    "30 18 * * *",
    "5 19 * * *",
    "30 19 * * *",
]


def today_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def chosen_slot(day=None):
    day = day or today_utc()
    digest = hashlib.sha256(day.encode()).hexdigest()
    return SLOTS[int(digest, 16) % len(SLOTS)]


def should_send():
    if os.environ.get("FORCE_SEND") == "true":
        return True

    slot = os.environ.get("SLOT", "").strip()
    if slot:
        return slot == chosen_slot()

    # A scheduled run with no SLOT must not send. A local run should.
    return os.environ.get("GITHUB_ACTIONS") != "true"


def explain():
    slot = os.environ.get("SLOT", "").strip()
    chosen = chosen_slot()
    lines = [f"Chosen slot for {today_utc()}: {chosen}"]

    if slot and slot not in SLOTS:
        lines.append(f"This run's slot {slot!r} is not listed in SLOTS.")
    elif os.environ.get("FORCE_SEND") == "true":
        lines.append("Manual run, so this run sends.")
    elif slot:
        if slot == chosen:
            lines.append(f"This run ({slot}) sends.")
        else:
            lines.append(f"This run ({slot}) does not send.")
    elif os.environ.get("GITHUB_ACTIONS") == "true":
        lines.append("Scheduled run has no slot, so it does not send.")
    else:
        lines.append("Local run, so this run sends.")
    return "\n".join(lines)


def get_message():
    return f"{random.choice(TEXTS)}{random.choice(EMOJIS)}"


def main():
    print(explain())
    if not should_send():
        print("Skipping send.")
        return

    api_id = int(os.environ["TG_API_ID"])
    api_hash = os.environ["TG_API_HASH"]
    session = os.environ["TG_SESSION"]
    recipient = os.environ["TG_RECIPIENT"]

    from telethon.sync import TelegramClient
    from telethon.sessions import StringSession

    PREPEND = "من عسل باتم🤖\nعرفان گفت بهت بگم: "
    message = PREPEND + get_message()
    print("Sending message...")
    with TelegramClient(StringSession(session), api_id, api_hash) as client:
        client.send_message(recipient, message)
    print(f"Sent message")


if __name__ == "__main__":
    if "--decide" in sys.argv:
        print(f"send={'true' if should_send() else 'false'}")
        print(explain(), file=sys.stderr)
    else:
        main()
