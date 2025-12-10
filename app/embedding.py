import os
import re
import time
import requests
from dotenv import load_dotenv

# Load API key from environment variable
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USE_LOCAL_EMBEDDING = os.getenv("USE_LOCAL_EMBEDDING", "false").lower() == "true"

# Try to import sentence-transformers for local embedding
try:
    from sentence_transformers import SentenceTransformer
    LOCAL_MODEL = SentenceTransformer('all-mpnet-base-v2')  # 768-dimensional model to match Pinecone index
    print("✅ Loaded local embedding model (all-mpnet-base-v2 - 768 dimensions)")
except ImportError:
    LOCAL_MODEL = None

def clean_text(text, max_length=5000):
    """Pre-process text before embedding: removes unwanted characters and limits length."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Invalid text input. Must be a non-empty string.")
    
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text[:max_length]  # Truncate if too long

def get_embedding(text, max_retries=5):
    """Generate an embedding using the Google Gemini API with retry logic, or fallback to local embedding."""
    
    if GEMINI_API_KEY is None:
        print("⚠️  GEMINI_API_KEY not set. Using local embedding fallback...")
        return get_local_embedding(text)
    
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
            time.sleep(2)  # Add delay after successful request to avoid rate limits
            return response.json()["embedding"]["values"]  # Extract embedding vector

        except requests.exceptions.RequestException as e:
            error_str = str(e)
            
            # Check for rate limit or quota errors
            if "429" in error_str or "quota" in error_str.lower() or "RESOURCE_EXHAUSTED" in error_str or "403" in error_str:
                print(f"⚠️  Gemini API error ({e}). Falling back to local embedding...")
                return get_local_embedding(text)
            
            # For other errors, retry with exponential backoff
            if attempt < max_retries - 1:
                wait_time = 3 ** attempt
                print(f"API error: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"⚠️  Max retries exceeded. Falling back to local embedding...")
                return get_local_embedding(text)
    
    print("Falling back to local embedding...")
    return get_local_embedding(text)

def get_local_embedding(text):
    """Fallback: Generate embedding using local sentence-transformers model (768-dimensional)."""
    global LOCAL_MODEL
    
    if LOCAL_MODEL is None:
        print("⚠️  Local embedding model not available. Installing sentence-transformers...")
        import subprocess
        subprocess.check_call(["pip", "install", "sentence-transformers"])
        from sentence_transformers import SentenceTransformer
        LOCAL_MODEL = SentenceTransformer('all-mpnet-base-v2')  # 768-dimensional model
    
    try:
        text = clean_text(text)
        embedding = LOCAL_MODEL.encode(text, convert_to_tensor=False)
        print(f"✅ Using local embedding (dimension: {len(embedding)})")
        return embedding.tolist()
    except Exception as e:
        print(f"❌ Local embedding failed: {e}")
        return None
