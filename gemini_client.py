import requests from config import GEMINI_API_KEY

def generate_tweet(): url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY data = { "contents": [{"parts": [{"text": "Generate 1 short, engaging, and fun tweet idea about crypto, web3, or airdrops."}]}] } response = requests.post(url, json=data) return response.json()['candidates'][0]['content']['parts'][0]['text']
