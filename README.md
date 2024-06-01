## short_story_api

This project involves creating a FastAPI application that interacts with a Supabase database to store character information and uses the OpenAI API to generate short stories based on these characters.

#### Step 1: Set Up Your Development Environment
Install Python: Ensure you have Python installed. You can download it from python.org.

#### Create a Project Directory:

`mkdir short_story_api` \
`cd short_story_api`

Set Up a Virtual Environment:
`python -m venv venv` \
`source venv/bin/activate` 

On Windows, use `venv\Scripts\activate`


#### Step 2: Install Required Packages
Install FastAPI and Uvicorn:
`pip install fastapi uvicorn`

Install Supabase and Dotenv:
`pip install supabase python-dotenv`


#### Step 3: Set Up Supabase
Create a Supabase Account: Go to Supabase, sign up or log in, and create a new project.

Create a Database Table:

Go to the "Database" section and create a table called "characters" with the following columns:
id: integer, primary key
name: text
details: text

Get Supabase Credentials:

Go to your project's settings to find the API URL and API Key. Note these down.


#### Step 4: Set Up Environment Variables
Create a `.env` File in your project directory and add your Supabase and OpenAI API keys:

`SUPABASE_URL=your_supabase_url`\
`SUPABASE_KEY=your_supabase_key`\
`OPENAI_API_KEY=your_openai_api_key`


#### Step 5: Obtain OpenAI API Key
Sign Up for OpenAI:

Go to OpenAI's website and sign up for an account.
Generate API Key:

After logging in, navigate to the API section of your account dashboard.
Create a new API key and copy it.
Add the key to your .env file as shown above.

#### Step 5.5: Migrate OpenAI Library (Important!)

Since ChatCompletion is no longer supported, we need to migrate your OpenAI library to use the newer API. Run the following command in your terminal:

`openai migrate`

This will update your existing code to use the functions and syntax compatible with the latest OpenAI library version.


#### Step 6: Write the FastAPI Application
Create main.py in your project directory and write the code to handle character creation and story generation


#### Step 7: Run Your Application
Start the FastAPI Server:
`uvicorn main:app --reload`

Open Your Browser: Go to `http://127.0.0.1:8000/docs` to access the automatically generated documentation for your API.


#### Step 8: Test Your Endpoints
Create a Character:

Send a POST request to `http://127.0.0.1:8000/api/characters` with a JSON body like:

{
  "name": "Bilbo Baggins",
  "details": "Hobbit lives in the Shire owning a magic ring"
}

###### Curl Command:

curl -X POST "http://127.0.0.1:8000/api/characters" -H "Content-Type: application/json" -d '{
  "name": "Bilbo Baggins",
  "details": "Hobbit lives in the Shire owning a magic ring"
}'


###### Expected Response:

{
  "id": 1,
  "name": "Bilbo Baggins",
  "details": "Hobbit lives in the Shire owning a magic ring"
}


###### Generate a Story:

Send a POST request to `http://127.0.0.1:8000/api/stories/generate_story` with a JSON body like:

{
  "character_name": "Bilbo Baggins"
}

or

{
  "character_id": 1
}

###### Curl Command with Character Name:

curl -X POST "http://127.0.0.1:8000/api/stories/generate_story" -H "Content-Type: application/json" -d '{
  "character_name": "Bilbo Baggins"
}'


###### Curl Command with Character ID:

curl -X POST "http://127.0.0.1:8000/api/stories/generate_story" -H "Content-Type: application/json" -d '{
  "character_id": 1
}'


###### Expected Response:

{
  "character": "Bilbo Baggins",
  "story": "Bilbo Baggins, a cheerful Hobbit lives in the Shire owning a magic ring, lived a quiet life. Unbeknownst to many, he owned a mysterious magic ring, which he stumbled upon during one of his adventures. This ring granted him the ability to become invisible, a secret he kept close to his heart. Though content with his simple life, he often daydreamed about the adventures the ring could lead him to. Little did he know, destiny had grand plans for him and his magical possession."
}


## Summary

1. Set Up Your Development Environment: Create a virtual environment and install necessary packages.
2. Set Up Supabase: Create an account, set up a project, and create a table for characters.
3. Obtain OpenAI API Key: Sign up for OpenAI, generate an API key, and store it in your .env file.
4. Write the FastAPI Application: Create main.py and write the code to handle character creation and story generation.
5. Run and Test the Application: Start the FastAPI server and test the endpoints using the automatically generated documentation.