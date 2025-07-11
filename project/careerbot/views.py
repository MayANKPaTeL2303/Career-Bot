import os
import requests
from django.shortcuts import render
from dotenv import load_dotenv
import markdown # type: ignore
import bleach

# Load environment variables from .env
load_dotenv()

# Constants
API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-1.5-flash-latest:generateContent?key={API_KEY}"
)

# Prompt Template
CAREER_GUIDANCE_TEMPLATE = """
You are an experienced and empathetic career guidance expert.

Based on the user's profile below, analyze their skills, interests, and education to suggest **three future-proof career paths** that align with current and emerging industry trends.

💡 Please follow these guidelines:
- Each suggestion should be unique and aligned with the user's background.
- Provide a clear, concise career **title** and a **1–2 paragraph description** explaining:
  - Why it's a good fit
  - Key skills or tools the user should focus on
  - Industry demand or growth prospects
- Include a helpful **link** to learn more or explore related jobs.

📋 Format your response exactly like this:
**Career Title(In h2 tag)** **:
    **New Line**
   Brief description with some bold important words(2–4 sentences).
    **New Line**
   (🔗 [Learn More about Career Title](URL))

 ...

 ...

Add a warm closing line to motivate the user:
"🌟 You’ve got this! Explore what excites you and build a future you love."

User Profile:
{user_profile}
"""

# Function to call Gemini API
def get_career_guidance(user_input):
    if not user_input.strip():
        return "⚠️ Please enter some input to get career suggestions."

    headers = {
        "Content-Type": "application/json"
    }

    prompt = CAREER_GUIDANCE_TEMPLATE.format(user_profile=user_input)

    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raises HTTPError for bad responses

        json_response = response.json()
        raw_text = json_response["candidates"][0]["content"]["parts"][0]["text"]
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(raw_text)

        # Sanitize the HTML file to prevent the XSS attack
        safe_html = bleach.clean(
            html_content,
            tags=["p", "strong", "b", "em", "a", "ul", "li", "ol", "br", "h1", "h2", "h3"],
            attributes={"a": ["href", "target"]},
            protocols=["http", "https"]
        )

        return safe_html

    except requests.exceptions.RequestException as e:
        return f"❌ Request failed: {str(e)}"

    except (KeyError, IndexError, TypeError):
        return "✅ Got a response, but couldn't parse the result properly. Please try again."

def resources(request):
    return render(request, 'careerbot/resources.html')

# Django view
def index(request):
    suggestion = None
    user_input = ""

    if request.method == "POST":
        user_input = request.POST.get("user_input", "").strip()
        if user_input:
            suggestion = get_career_guidance(user_input)
        else:
            suggestion = "⚠️ Input cannot be empty. Please describe your profile."

    return render(request, "careerbot/index.html", {
        "suggestion": suggestion,
        "user_input": user_input
    })
