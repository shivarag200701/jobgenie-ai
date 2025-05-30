import ast
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

Only respond with a **valid JSON object** like this:

{{
  "tailoredResume": "...",
  "coverLetter": "...",
  "fitSummary": "..."
}}
⚠️ Do not include any extra text, explanations, or markdown. Output only raw JSON, nothing else.
"""

    # Call the OpenAI Chat API
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
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
        try:
            # Try safer literal evaluation
            result = ast.literal_eval(content)
            return result
        except Exception:
            return {
                "tailoredResume": "",
                "coverLetter": "",
                "fitSummary": "Could not parse model output. Here's the raw content:",
                "raw": content,
            }
