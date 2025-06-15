import requests
import hashlib
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
APPROVAL_STORE = {}  # Menyimpan tweet sementara berdasarkan message_id

def short_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]  # hash aman max 64 karakter

def send_for_approval(tweet_text):
    tweet_hash = short_hash(tweet_text)
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"📝 *Review this tweet:*\n\n{tweet_text}",
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [[
                {"text": "✅ Approve", "callback_data": f"approve::{tweet_hash}"},
                {"text": "❌ Reject", "callback_data": f"reject::{tweet_hash}"}
            ]]
        }
    }

    resp = requests.post(url, json=data).json()

    if "result" in resp and "message_id" in resp["result"]:
        message_id = resp["result"]["message_id"]
        APPROVAL_STORE[tweet_hash] = tweet_text
    else:
        print("❌ Gagal kirim ke Telegram:", resp)

def handle_callback(update):
    callback = update.get("callback_query", {})
    data = callback.get("data")
    message = callback.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    callback_id = callback.get("id")

    if "::" in data:
        action, tweet_hash = data.split("::", 1)

        if action == "approve":
            from twitter_client import post_tweet
            tweet_text = APPROVAL_STORE.get(tweet_hash)
            if tweet_text:
                success = post_tweet(tweet_text)
                text = "✅ Tweet posted successfully!" if success else "❌ Failed to post tweet."
            else:
                text = "⚠️ Tweet not found in memory."

        elif action == "reject":
            text = "❌ Tweet rejected."

        else:
            text = "⚠️ Unknown action."

        # Kirim respons ke Telegram
        requests.post(f"{BASE_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })

        # Hapus dari store
        if tweet_hash in APPROVAL_STORE:
            APPROVAL_STORE.pop(tweet_hash)

    # Acknowledge button click
    if callback_id:
        requests.post(f"{BASE_URL}/answerCallbackQuery", json={
            "callback_query_id": callback_id
        })