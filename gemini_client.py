import requests from config import GEMINI_API_KEY import time

API_KEYS = GEMINI_API_KEY.split(",") current_key_index = 0

def generate_tweet(): global current_key_index for _ in range(len(API_KEYS)): use_key = API_KEYS[current_key_index] url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={use_key}" data = { "contents": [{"parts": [{"text": "Generate 1 short, engaging, and fun tweet idea about crypto, web3, or airdrops."}]}] } try: response = requests.post(url, json=data, timeout=10) result = response.json()

if 'candidates' in result:
            return result['candidates'][0]['content']['parts'][0]['text']
        elif 'error' in result and result['error'].get('code') == 429:
            print(f"API key {current_key_index + 1} quota exceeded. Switching key...")
            current_key_index = (current_key_index + 1) % len(API_KEYS)
            time.sleep(1)
        else:
            print("Gemini response error:", result)
            break
    except Exception as e:
        print("Gemini API error:", e)
        current_key_index = (current_key_index + 1) % len(API_KEYS)
        time.sleep(1)

raise Exception("All Gemini API keys exhausted or failed.")

