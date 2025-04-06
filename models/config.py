import os
from dotenv import load_dotenv
load_dotenv()


GOOGLE_SEARCH_API = os.getenv("GOOGLE_SEARCH_API")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
PINECONE_INDEX_NAME = "web-scraped-data"
PINECONE_ADS_INDEX_NAME = "generated-ad"


