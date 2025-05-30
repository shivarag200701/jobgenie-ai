import os

from ai_engine import generate_outputs
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


# Request schema to validate and parse JSON in python objects using pydantic
class GenRequest(BaseModel):
    resume: str
    job_description: str


# POST endpoint for AI generation
@app.post("/generate")
async def generate(data: GenRequest):
    result = generate_outputs(data.resume, data.job_description)
    return result
