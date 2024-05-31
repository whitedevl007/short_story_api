from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import supabase
import openai
import backoff
from openai.error import RateLimitError

# Load environment variables from .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the router with a prefix
router = APIRouter(prefix="/api/stories")

class GenerateStoryRequest(BaseModel):
    character_name: Optional[str] = None
    character_id: Optional[int] = None

@backoff.on_exception(backoff.expo, RateLimitError, max_time=120, base=2)
def generate_story_with_backoff(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=20,
    )
    return response

@router.post("/generate_story", status_code=status.HTTP_201_CREATED)
def generate_story(request: GenerateStoryRequest):
    if request.character_id is not None:
        response = supabase_client.table('characters').select('*').eq('id', request.character_id).execute()
    elif request.character_name is not None:
        response = supabase_client.table('characters').select('*').eq('name', request.character_name).execute()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Character name or id must be provided.")

    # Logging the response for debugging
    print("Supabase response:", response)

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

    # Generate the story using OpenAI's API with backoff for rate limit errors
    try:
        response = generate_story_with_backoff(prompt)
        story = response.choices[0].message['content'].strip()
        return {"character": character_name, "story": story}

    except RateLimitError as e:
        # Handle RateLimitError appropriately (already handled by backoff, but logging can be added if necessary)
        print(f"Rate limit error: {e}")
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="OpenAI rate limit reached. Please try again later.")

    except openai.error.OpenAIError as e:
        # Handle other OpenAI errors
        print(f"OpenAI error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error generating story: {e}")

    except Exception as e:
        # Handle other exceptions
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")
