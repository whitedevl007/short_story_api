from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI


import os
from supabase import create_client, Client
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configure OpenAI
# Your OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create OpenAI client object with your API key
client = OpenAI(api_key=OPENAI_API_KEY)


class Character(BaseModel):
    name: str
    details: str

@app.post("/api/create_character", status_code=status.HTTP_201_CREATED)
def create_character(character: Character):
    response = supabase.table('characters').insert({"name": character.name, "details": character.details}).execute()
    if response.error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.error.message)
    return {"id": response.data[0].id, "name": character.name, "details": character.details}

class GenerateStoryRequest(BaseModel):
    character_name: Optional[str] = None
    character_id: Optional[int] = None

@app.post("/api/generate_story", status_code=status.HTTP_201_CREATED)
def generate_story(request: GenerateStoryRequest):
    if request.character_id is not None:
        response = supabase.table('characters').select('*').eq('id', request.character_id).execute()
    elif request.character_name is not None:
        response = supabase.table('characters').select('*').eq('name', request.character_name).execute()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Character name or id must be provided.")

    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found.")

    character = response.data[0]
    character_name = character['name']
    character_details = character['details']

    prompt = (
        f"{character_name}, a cheerful {character_details}, lived a quiet life. "
        "Unbeknownst to many, he owned a mysterious magic ring, which he stumbled upon during one of his adventures. "
        "This ring granted him the ability to become invisible, a secret he kept close to his heart. "
        "Though content with his simple life, he often daydreamed about the adventures the ring could lead him to. "
        "Little did he know, destiny had grand plans for him and his magical possession."
    )

    # Update to use client.completions.create
    response = client.completions.create(
        engine="text-davinci-003",  # Replace with your preferred engine
        prompt=prompt,
        max_tokens=100,
        n=1,  # Number of completions (set to 1 for single story)
        stop=None,  # Optional stop sequence to indicate end of story
        temperature=0.7  # Adjust temperature for creativity vs. coherence
    )


    story = response.choices[0].text.strip()
    return {"character": character_name, "story": story}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
