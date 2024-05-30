from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    """Simple health check endpoint to verify API is running."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)