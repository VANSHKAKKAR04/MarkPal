import os
import re
import time
import requests

# Load API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def clean_text(text, max_length=5000):
    """Pre-process text before embedding: removes unwanted characters and limits length."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Invalid text input. Must be a non-empty string.")
    
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text[:max_length]  # Truncate if too long

def get_embedding(text, max_retries=5):
    """Generate an embedding using the Google Gemini API with retry logic."""
    
    if GEMINI_API_KEY is None:
        raise ValueError("GEMINI_API_KEY is not set. Please check your environment variables.")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    try:
        text = clean_text(text)  # Clean input text
    except ValueError as e:
        print(f"Preprocessing Error: {e}")
        return None  

    data = {
        "content": {"parts": [{"text": text}]}
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["embedding"]["values"]  # Extract embedding vector

        except requests.exceptions.RequestException as e:
            wait_time = 3 ** attempt  # Exponential backoff
            print(f"API error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    print("Max retries exceeded for embedding API.")
    return None  # Return None on failure
