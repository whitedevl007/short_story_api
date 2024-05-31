# from fastapi import FastAPI, HTTPException, status
# from pydantic import BaseModel
# from supabase import create_client, Client
# from dotenv import load_dotenv
# import os
# import openai
# from typing import Optional
# from time import time , sleep

# app = FastAPI()

# # Load environment variables from .env file
# load_dotenv()

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Initialize Supabase client
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # Configure OpenAI
# openai.api_key = OPENAI_API_KEY

# class Character(BaseModel):
#     name: str
#     details: str

# @app.post("/api/create_character", status_code=status.HTTP_201_CREATED)
# def create_character(character: Character):
#     response = supabase.table('characters').insert({"name": character.name, "details": character.details}).execute()

#     # Logging the response for debugging
#     print("Supabase response:", response)

#     if response.data:
#         return {"id": response.data[0]['id'], "name": character.name, "details": character.details}
#     else:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.error_message if response.error else "Unknown error")

# class GenerateStoryRequest(BaseModel):
#     character_name: Optional[str] = None
#     character_id: Optional[int] = None

# @app.post("/api/generate_story", status_code=status.HTTP_201_CREATED)
# def generate_story(request: GenerateStoryRequest):
#     if request.character_id is not None:
#         response = supabase.table('characters').select('*').eq('id', request.character_id).execute()
#     elif request.character_name is not None:
#         response = supabase.table('characters').select('*').eq('name', request.character_name).execute()
#     else:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Character name or id must be provided.")

#     # Logging the response for debugging
#     print("Supabase response:", response)

#     if not response.data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found.")

#     character = response.data[0]
#     character_name = character['name']
#     character_details = character['details']

#     prompt = (
#         f"{character_name}, a cheerful {character_details}, lived a quiet life. "
#         "Unbeknownst to many, he owned a mysterious magic ring, which he stumbled upon during one of his adventures. "
#         "This ring granted him the ability to become invisible, a secret he kept close to his heart. "
#         "Though content with his simple life, he often daydreamed about the adventures the ring could lead him to. "
#         "Little did he know, destiny had grand plans for him and his magical possession."
#     )

#     # Generate the story using OpenAI's API
#     max_retries = 3  # Set a maximum number of retries
#     retry_count = 0
#     while True:
#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=100,
#             )
#             story = response.choices[0].message['content'].strip()
#             return {"character": character_name, "story": story}

#         except openai.error.RateLimitError as e:
#             retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
#             print(f"Rate limit exceeded. Retrying after {retry_time} seconds...")
#             sleep(retry_time)
#             retry_count += 1

#             if retry_count >= max_retries:
#                 raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="OpenAI rate limit reached.")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



from fastapi import FastAPI
from dotenv import load_dotenv
import os
from routers import characters, stories


app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app.include_router(characters.router)
app.include_router(stories.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

