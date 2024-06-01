from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from supabase import Client, create_client
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/characters")

# Initialize the Supabase client once
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

class Character(BaseModel):
    name: str
    details: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_character(character: Character):
    response = supabase.table('characters').insert({"name": character.name, "details": character.details}).execute()

    # Logging the response for debugging
    print("Supabase response:", response)

    if response.data:
        return {"id": response.data[0]['id'], "name": character.name, "details": character.details}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.error_message if response.error else "Unknown error")
