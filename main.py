from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import openai
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
openai.api_key = OPENAI_API_KEY

class Character(BaseModel):
    name: str
    details: str

@app.post("/api/create_character")
def create_character(character: Character):
    response = supabase.table('characters').insert({"name": character.name, "details": character.details}).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"id": response.data[0]['id'], "name": character.name, "details": character.details}

class GenerateStoryRequest(BaseModel):
    character_name: Optional[str] = None
    character_id: Optional[int] = None

@app.post("/api/generate_story")
def generate_story(request: GenerateStoryRequest):
    if request.character_id is not None:
        response = supabase.table('characters').select('*').eq('id', request.character_id).execute()
    elif request.character_name is not None:
        response = supabase.table('characters').select('*').eq('name', request.character_name).execute()
    else:
        raise HTTPException(status_code=400, detail="Character name or id must be provided.")

    if not response.data:
        raise HTTPException(status_code=404, detail="Character not found.")

    character = response.data[0]
    prompt = (
        f"{character['name']}, a cheerful {character['details']}, lived a quiet life. "
        "Unbeknownst to many, he owned a mysterious magic ring, which he stumbled upon during one of his adventures. "
        "This ring granted him the ability to become invisible, a secret he kept close to his heart. "
        "Though content with his simple life, he often daydreamed about the adventures the ring could lead him to. "
        "Little did he know, destiny had grand plans for him and his magical possession."
    )

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    story = response.choices[0].text.strip()
    return {"character": character['name'], "story": story}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
