import httpx
import json

# Replace with your actual Google AI Studio API key
API_KEY = "GOOGLE_API_KEY"
MODEL_NAME = "gemini-1.5-flash-latest"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

PROMPT_TEMPLATE = """
You are an expert AI assistant for a resume screening system. Your sole task is to provide a concise, 1-2 sentence professional feedback summary for a recruiter after analyzing a resume against a job description.
**CRITICAL INSTRUCTIONS:**
- Provide only the feedback text.
- DO NOT add any introductory text, conversational remarks, or any other content.

**Job Description:**
---
{jd_text}
---

**Resume:**
---
{resume_text}
---
"""

def load_model():
    """
    Checks if the Gemini API key is properly set. This function is called by app.py on startup.
    """
    print("Checking for Gemini API key...")
    if not API_KEY or "REPLACE" in API_KEY:
        raise ValueError("API_KEY is not configured. Please replace the placeholder in services/llm_service.py.")
    print("Gemini API key is configured.")

async def get_llm_feedback(resume_text: str, jd_text: str) -> str:
    """
    Calls the Google Gemini API to get qualitative feedback.
    """
    headers = {'Content-Type': 'application/json'}
    params = {'key': API_KEY}
    
    formatted_prompt = PROMPT_TEMPLATE.format(jd_text=jd_text, resume_text=resume_text)
    
    payload = {
        "contents": [{
            "parts": [{"text": formatted_prompt}]
        }]
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(API_URL, headers=headers, params=params, json=payload)
            response.raise_for_status() 
            
            response_data = response.json()
            feedback = response_data['candidates'][0]['content']['parts'][0]['text']
            return feedback.strip()
            
    except httpx.HTTPStatusError as e:
        print(f"Error calling Gemini API: {e.response.status_code} {e.response.text}")
        return "Failed to get a response from the AI service."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred during AI feedback generation."

