import os
import requests
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

def get_career_guidance(user_input):
    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are a professional career guidance expert.
    Analyze the user's profile below and suggest 3 suitable, future-proof career options...

    User Profile:
    {user_input}

    Response format:
    1. **Career Title**  
       Description  
       🔗 [Link Text](URL)

    2. ...
    3. ...
    Add a closing line: "🌟 You’ve got this! Explore what excites you and build a future you love."
    """

    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "✅ Got response but couldn't parse it properly."
    else:
        return f"❌ Error {response.status_code}: {response.text}"

def index(request):
    suggestion = None
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        if user_input:
            suggestion = get_career_guidance(user_input)
        return render(request, "careerbot/index.html", {"suggestion": suggestion, "user_input": user_input})
    return render(request, "careerbot/index.html")
