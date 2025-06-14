import os

from ai_engine import (
    classify_role_with_llm,
    extract_skills,
    generate_outputs,
    retrieve_relevant_chunks,
    store_resume_chunks,
)
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# load the env variables
load_dotenv()


print("OpenAI Key Loaded:", os.getenv("OPENAI_API_KEY"))
# create an istnace of app
app = FastAPI()

# Allow connection between frontend and backend: localhost:5173 for vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for dev
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


# Request schema to validate and parse JSON in python objects using pydantic for reponse based only on prompt
class GenRequest(BaseModel):
    resume: str
    job_description: str


# Request schema to validate and parse JSON in python objects using pydantic for classify job role
class ClassifyRequest(BaseModel):
    job_description: str


# Request schema to validate and parse JSON in python objects using pydantic for extract key requirements
class KeyRequirements(BaseModel):
    job_description: str


# Request schema to validate and parse JSON in python objects using pydantic for extract relevant resume chunks
class ChunkRequest(BaseModel):
    job_description: str
    resume: str


# POST endpoint for AI generation
@app.post("/generate")
async def generate(data: GenRequest):
    result = generate_outputs(data.resume, data.job_description)
    return result


# POST endpoint for job role classification
@app.post("/classify-role")
async def classify(data: ClassifyRequest):
    result = classify_role_with_llm(data.job_description)
    return result


# POST endpoint to extract key requirements
@app.post("/key_requirements")
async def requirements(data: KeyRequirements):
    print(data.job_description)
    result = extract_skills(data.job_description)
    return result


# POST endpoint to retrive relevant resume chunks
@app.post("/retrive_chunks")
async def get_matching_chunks(data: ChunkRequest):
    collection, _ = store_resume_chunks(data.resume)
    top_chunks = retrieve_relevant_chunks(data.job_description, collection)
    return {"top_chunks": top_chunks}
