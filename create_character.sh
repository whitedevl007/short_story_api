#!/bin/bash

# Prompt the user for character name
read -p "Enter character name: " name

# Prompt the user for character details
read -p "Enter character details: " details

# Construct the JSON data using the user input
data="{\"name\": \"$name\", \"details\": \"$details\"}"

# Send the POST request using curl
curl -X POST 'https://mtrrbsymkweoysvlbqya.supabase.co/rest/v1/characters' \
  -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im10cnJic3lta3dlb3lzdmxicXlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwNjYyNjEsImV4cCI6MjAzMjY0MjI2MX0.6mT0QlZc7e1al0CI3nN5eYP676xg4EFYwXsC4YR2vSA" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im10cnJic3lta3dlb3lzdmxicXlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwNjYyNjEsImV4cCI6MjAzMjY0MjI2MX0.6mT0QlZc7e1al0CI3nN5eYP676xg4EFYwXsC4YR2vSA" \
  -H "Content-Type: application/json" \
  -d "$data"

echo "Character data sent!"

