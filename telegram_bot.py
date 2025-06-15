<<<<<<< HEAD
import requests from config
import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
=======
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
>>>>>>> 2e551c3 (Tambahkan deskripsi singkat tentang perubahan kamu di sini)

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
APPROVAL_STORE = {}  # Menyimpan tweet sementara berdasarkan message_id

def send_for_approval(tweet_text):
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"📝 *Review this tweet:*\n\n{tweet_text}",
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [[
                {"text": "✅ Approve", "callback_data": f"approve::{tweet_text}"},
                {"text": "❌ Reject", "callback_data": "reject"}
            ]]
        }
    }

    resp = requests.post(url, json=data).json()

    # Simpan tweet di memory sementara
    if "result" in resp and "message_id" in resp["result"]:
        message_id = resp["result"]["message_id"]
        APPROVAL_STORE[message_id] = tweet_text
    else:
        print("❌ Gagal kirim ke Telegram:", resp)

def handle_callback(update):
    callback = update.get("callback_query", {})
    data = callback.get("data")
    message = callback.get("message", {})
    message_id = message.get("message_id")
    chat_id = message.get("chat", {}).get("id")

    if data.startswith("approve::"):
        from twitter_client import post_tweet

        tweet_text = data.split("approve::", 1)[1]
        success = post_tweet(tweet_text)

        text = "✅ Tweet posted successfully!" if success else "❌ Failed to post tweet."

        # Balasan ke Telegram
        requests.post(f"{BASE_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })

    elif data == "reject":
        requests.post(f"{BASE_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": "❌ Tweet rejected."
        })

    # Hapus dari store jika ada
    if message_id in APPROVAL_STORE:
        APPROVAL_STORE.pop(message_id)

    # Acknowledge button click
    callback_id = callback.get("id")
    if callback_id:
        requests.post(f"{BASE_URL}/answerCallbackQuery", json={
            "callback_query_id": callback_id
        })