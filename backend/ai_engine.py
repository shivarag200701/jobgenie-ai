import ast
import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print("OpenAI Key Loaded:", api_key[:8] + "..." if api_key else "None")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


# Function to generate result only based on LLM and no AI agents
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


# Function to classify roles for Step 1 of AI-agents
def classify_role_with_llm(job_description: str):
    system_prompt = """
    You are a job role classification expert. Based on the given job description text, classify the user's most relevant tech job title from this list:
    - Backend Developer
    - Frontend Developer
    - Full Stack Developer
    - DevOps Engineer
    - Data Scientist
    - Machine Learning Engineer
    - MLOps Engineer
    - Software Engineer
    - AI Research Engineer
    - Cloud Engineer
    - Cybersecurity Analyst
    - QA Engineer
    - Embedded Systems Engineer
    - Product Engineer
    Return only the most likely job title.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": job_description},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


# Function to find "Required skills" , "responsiblities" and "nice to have"


def extract_skills(job_description: str):
    print("📄 JD Input:", job_description)

    system_prompt = """
You are an AI that extracts job requirements.
Return a valid JSON like:
{
  "required_skills": ["skill1", "skill2"],
  "responsibilities": ["task1", "task2"],
  "nice_to_have": ["bonus1", "bonus2"]
}
Do not include any explanation or extra text.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": job_description},
        ],
        temperature=0.4,
    )

    content = response.choices[0].message.content
    print("🧠 Raw content:", content)

    # Strip markdown code block formatting if present
    content = re.sub(
        r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.MULTILINE
    )

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "required_skills": [],
            "responsibilities": [],
            "nice_to_have": [],
            "raw": content,
        }
