import requests from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

APPROVAL_STORE = {}  # {message_id: tweet_text}

def send_for_approval(tweet_text): url = f"{BASE_URL}/sendMessage" data = { "chat_id": TELEGRAM_CHAT_ID, "text": f"Review this tweet:\n\n{tweet_text}", "reply_markup": { "inline_keyboard": [[ {"text": "✅ Approve", "callback_data": f"approve"}, {"text": "❌ Reject", "callback_data": f"reject"} ]] } } resp = requests.post(url, json=data).json() APPROVAL_STORE[resp['result']['message_id']] = tweet_text

def handle_callback(update): message_id = update['callback_query']['message']['message_id'] action = update['callback_query']['data'] if action == "approve": from twitter_client import post_tweet tweet_text = APPROVAL_STORE.pop(message_id, None) if tweet_text: post_tweet(tweet_text) requests.post(f"{BASE_URL}/sendMessage", json={ "chat_id": TELEGRAM_CHAT_ID, "text": "✅ Tweet posted successfully!" }) elif action == "reject": requests.post(f"{BASE_URL}/sendMessage", json={ "chat_id": TELEGRAM_CHAT_ID, "text": "❌ Tweet rejected." }) APPROVAL_STORE.pop(message_id, None)
