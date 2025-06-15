from gemini_client import generate_tweet
from telegram_bot import send_for_approval

if __name__ == "__main__":
    tweet = generate_tweet()
    print("Generated Tweet:", tweet)
    send_for_approval(tweet)