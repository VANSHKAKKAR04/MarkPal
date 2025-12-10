import requests
import os
from dotenv import load_dotenv

# Explicitly load .env file
load_dotenv()

API_KEY = os.getenv("GOOGLE_SEARCH_API")
CX_ID = os.getenv("GOOGLE_CSE_ID")

def google_search(query, num_results=5):
    """Search Google Custom Search API and return a list of URLs."""
    print(f"🔧 Debug - Using API Key: {API_KEY[:20]}..." if API_KEY else "🔧 Debug - API Key: NOT SET")
    print(f"🔧 Debug - Using CX ID: {CX_ID}")
    print(f"🔧 Debug - Query: {query}\n")
    
    url = f"https://customsearch.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": CX_ID,
        "num": num_results,
        "key": API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        
        data = response.json()
        
        if "items" in data:
            return [item["link"] for item in data["items"]]
        else:
            print("❌ No search results found.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"⚠️ API Request Error: {e}")
        return []
