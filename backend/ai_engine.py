import ast
import json
import os
import re
import uuid

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from utlis.text_splitter import split_text

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print("OpenAI Key Loaded:", api_key[:8] + "..." if api_key else "None")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# init Chroma Client
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("resume_chunks")


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


##Agentic workflow
""" step1 - Classify the job role
    step2 - Extract Key Requirements
    step3 - Retrieve matching Resume Segments (RAG)
    step4 - Tailor resume based on matching resume segments for more accuracy
"""


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


# Function to find "Required skills" , "responsiblities" and "nice to have" Step 2
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


# Step 3 - Retrieve matching Resume Segments (RAG)


# embed using openai embedding
def embed_text(text: str):
    reponse = client.embeddings.create(input=[text], model="text-embedding-ada-002")
    return reponse.data[0].embedding


# Store resume chunks in Chroma
def store_resume_chunks(resume_text: str):
    # Create a temporary collection (in-memory)
    temp_collection = chroma_client.create_collection(name=f"resume_{uuid.uuid4()}")

    chunks = split_text(resume_text)
    embeddings = [embed_text(chunk) for chunk in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    temp_collection.add(ids=ids, embeddings=embeddings, documents=chunks)
    print(chunks)

    return (
        temp_collection,
        chunks,
    )  # ⬅️ return collection for reuse= [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(ids=ids, embeddings=embeddings, documents=chunks)
    print(chunks)
    return chunks


# Retrieve matching resume segments
def retrieve_relevant_chunks(job_description: str, collection, top_k: int = 5):
    query_embedding = embed_text(job_description)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )
    print(results["documents"][0])
    return results["documents"][0]  # return the top k chunks
