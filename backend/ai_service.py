import os
import json
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

# Read API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Create Gemini client
client = genai.Client(api_key=API_KEY)

def analyze_resume(resume_text: str):
    """
    Analyze resume and return structured JSON.
    """

    prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze this resume.

Resume:

{resume_text}

Return ONLY valid JSON.

Use this exact format:

{{
    "resume_score": 90,
    "technical_skills": [],
    "missing_skills": [],
    "career_recommendations": [],
    "resume_improvements": []
}}

Do not write markdown.
Do not use ```json.
Return only JSON.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown if present
    text = text.replace("```json", "")
    text = text.replace("```", "")

    return json.loads(text)