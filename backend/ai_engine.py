import json
import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print("OpenAI Key Loaded:", api_key[:8] + "..." if api_key else "None")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


def generate_outputs(resume: str, job_description: str):
    prompt = f"""
You are a helpful assistant that tailors a resume and cover letter based on a given resume and job description.

Resume:
{resume}

Job Description:
{job_description}

---

Return a JSON object with the following structure (no explanation, only JSON):

{{
  "tailoredResume": "...",
  "coverLetter": "...",
  "fitSummary": "..."
}}
"""

    # Call the OpenAI Chat API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    # Extract and parse the JSON result
    content = response.choices[0].message.content

    try:
        result = json.loads(content)
        return result
    except json.JSONDecodeError:
        # fallback: return raw string if not parseable
        return {
            "tailoredResume": "",
            "coverLetter": "",
            "fitSummary": "Could not parse model output. Here's the raw content:",
            "raw": content,
        }
