import requests
import time
from config import GEMINI_API_KEY

# Pisahkan beberapa API key dengan koma di GitHub Secret
API_KEYS = GEMINI_API_KEY.split(",")
current_key_index = 0

def generate_tweet():
    global current_key_index

    for _ in range(len(API_KEYS)):
        use_key = API_KEYS[current_key_index]
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={use_key}"
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Generate 1 short, engaging, and fun tweet idea about crypto, web3, or airdrops."
                        }
                    ]
                }
            ]
        }

        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()

            # Cek jika respons valid
            if "candidates" in result:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                # Ganti ke API key berikutnya jika gagal
                current_key_index = (current_key_index + 1) % len(API_KEYS)

        except Exception as e:
            # Tangani error & coba key berikutnya
            current_key_index = (current_key_index + 1) % len(API_KEYS)

        # Delay opsional untuk hindari rate-limit
        time.sleep(1)

    return "Tweet generation failed after rotating all keys."
