import os
import json
from dotenv import load_dotenv
from google import genai

# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv()

# Read Gemini API Key from .env file
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# Create Gemini Client
client = genai.Client(api_key=API_KEY)


# =====================================================
# Helper Function
# Converts Gemini response into JSON safely
# =====================================================

def parse_json_response(text: str):
    """
    Removes markdown formatting (if Gemini returns it)
    and converts the response into a Python dictionary.
    """

    text = text.strip()

    # Remove markdown code blocks if present
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    return json.loads(text)


# =====================================================
# Resume Analysis
# =====================================================

def analyze_resume(resume_text: str):
    """
    Analyze a resume using Gemini AI.

    Returns:
    - Resume Score
    - Technical Skills
    - Missing Skills
    - Career Recommendations
    - Resume Improvements
    """

    prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze the following resume.

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

Do not use markdown.
Return only JSON.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return parse_json_response(response.text)


# =====================================================
# Resume vs Job Description Matching
# =====================================================

def match_resume_with_job(
    resume_text: str,
    job_description: str
):
    """
    Compare the uploaded resume with
    the latest uploaded job description.

    Returns:
    - Match Score
    - Matching Skills
    - Missing Skills
    - Recommendations
    """

    prompt = f"""
You are an AI Career Advisor.

Compare the following resume with the job description.

Resume:

{resume_text}

Job Description:

{job_description}

Return ONLY valid JSON.

Use this format:

{{
    "match_score":85,
    "matching_skills":[],
    "missing_skills":[],
    "recommendations":[]
}}

Do not use markdown.
Return only JSON.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return parse_json_response(response.text)

# =====================================================
# AI Interview Question Generator
# =====================================================

def generate_interview_questions(
    resume_text: str,
    job_description: str
):
    """
    Generate interview questions based on the
    student's resume and job description.

    Returns:
    - Technical Questions
    - Behavioral Questions
    - HR Questions
    - Coding Questions
    """

    prompt = f"""
You are an experienced Technical Interviewer.

Based on the resume and job description below,
generate interview questions.

Resume:

{resume_text}

Job Description:

{job_description}

Return ONLY valid JSON.

Use exactly this format:

{{
    "technical": [
        {{
            "question": "",
            "answer": "",
            "difficulty": ""
        }}
    ],
    "behavioral": [
        {{
            "question": "",
            "answer": "",
            "difficulty": ""
        }}
    ],
    "hr": [
        {{
            "question": "",
            "answer": "",
            "difficulty": ""
        }}
    ],
    "coding": [
        {{
            "question": "",
            "answer": "",
            "difficulty": ""
        }}
    ]
}}

Requirements:

- Generate 5 technical questions.
- Generate 3 behavioral questions.
- Generate 3 HR questions.
- Generate 2 coding questions.
- Difficulty must be Easy, Medium, or Hard.
- Answers should be concise and suitable for interview preparation.
- Return only JSON.
- Do not use markdown.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return parse_json_response(response.text)