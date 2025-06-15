from gemini_client import generate_tweet from telegram_bot import send_for_approval

def run_bot(): tweet = generate_tweet() send_for_approval(tweet)

if name == "main": run_bot()
