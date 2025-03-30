import google.generativeai as genai
from config import GEMINI_API_KEY
from database.pinecone_db import query_pinecone

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def generate_ad(product):
    """Generates an ad for a product using Gemini 1.5 Flash based on retrieved reviews."""
    reviews = query_pinecone(product, top_k=5)

    # Handle cases where no reviews are found
    if not reviews:
        print(f"⚠️ No reviews found for {product}. Using a generic ad prompt.")
        reviews_text = "No reviews available. Write a general compelling ad."
    else:
        reviews_text = "\n".join(reviews)

    prompt = f"Write a compelling ad for {product} based on these reviews:\n\n{reviews_text}"

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text if hasattr(response, "text") else "⚠️ Failed to generate ad."
    
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return "⚠️ An error occurred while generating the ad."

