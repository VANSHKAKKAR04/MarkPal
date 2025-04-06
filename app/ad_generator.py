import google.generativeai as genai
from app.config import GEMINI_API_KEY
from pinecone_db import query_pinecone, store_ad_in_pinecone, query_ad_pinecone

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def generate_ad(product, force_regenerate=False):
    """
    Generates an ad for a product using Gemini 1.5 Flash based on retrieved reviews.
    Implements Retrieval-Augmented Generation (RAG) with Pinecone.
    Make sure the Ad has the appropriate trust signals, urgency and call to action 
    Parameters:
      product (str): The product name.
      force_regenerate (bool): If True, regenerates the ad even if one exists.
    
    Returns:
      str: The generated advertisement.
    """
    # Check if an ad already exists in Pinecone unless we're forcing a regeneration.
    if not force_regenerate:
        existing_ads = query_ad_pinecone(product)
        if existing_ads:
            # Verify if the retrieved ad appears to match the product
            if any(product.lower() in ad.lower() for ad in existing_ads):
                print(f"✅ Retrieved existing ad for {product} from Pinecone.")
                return existing_ads[0]
            else:
                print("ℹ️ Existing ad found but does not seem to match the product; regenerating.")

    # Retrieve relevant reviews from the Pinecone vector database
    reviews = query_pinecone(product, top_k=5)

    # Handle cases where no reviews are found
    if not reviews:
        print(f"⚠️ No reviews found for {product}. Using a generic ad prompt.")
        reviews_text = "No reviews available. Write a general, compelling ad for the product."
    else:
        reviews_text = "\n".join(reviews)

    # Construct an enhanced prompt with retrieval-augmented context
    prompt = f"""
You are an expert ad copywriter. Create a compelling advertisement for the product: "{product}".

Base your ad on the following customer reviews and insights:
{reviews_text}

Ensure the ad is engaging, persuasive, and accurately highlights the best aspects of the product.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        ad_text = response.text if hasattr(response, "text") else "⚠️ Failed to generate ad."

        # Optionally, warn if the generated ad doesn't reference the product name
        if product.lower() not in ad_text.lower():
            print("⚠️ Warning: The generated ad does not appear to mention the product properly.")

        # Store the generated ad in Pinecone for future retrieval
        store_ad_in_pinecone(product, ad_text)

        return ad_text

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return "⚠️ An error occurred while generating the ad."
