import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
headers = {"Content-Type": "application/json"}
data = {
    "contents": [{"parts": [{"text": "Hello, who are you?"}]}]
}

res = requests.post(url, headers=headers, json=data)
print(res.status_code)
print(res.text)
