import google.generativeai as genai
from config import GEMINI_API_KEY
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
        # Preferred model: try Gemini; some projects or API plans may not support every model name.
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            ad_text = response.text if hasattr(response, "text") else None
        except Exception:
            # If the preferred model isn't available for this API version/plan, try a more compatible approach
            try:
                model = genai.GenerativeModel("text-bison@001")
                response = model.generate_content(prompt)
                ad_text = response.text if hasattr(response, "text") else None
            except Exception as inner_e:
                # Re-raise the inner exception to be caught by outer handler and trigger fallback
                raise inner_e

        if not ad_text:
            raise RuntimeError("Empty response from generative model")

        if product.lower() not in ad_text.lower():
            print("⚠️ Warning: The generated ad does not appear to mention the product properly.")

        # Store the generated ad in Pinecone for future retrieval
        store_ad_in_pinecone(product, ad_text)
        return ad_text

    except Exception as e:
        print(f"❌ Gemini API Error or unsupported model: {e}")
        print("⚠️ Falling back to local/template ad generator.")
        # Local fallback: simple template-based RAG-style generation using retrieved reviews
        def local_generate_ad(product_name, reviews_list):
            # Basic heuristics: pick up to 3 strongest review snippets and build a short ad
            snippets = []
            if isinstance(reviews_list, str):
                text = reviews_list
                # split into sentences and take the first few non-empty ones
                parts = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
                snippets = parts[:3]
            elif isinstance(reviews_list, list):
                # take first sentence from each review up to 3
                for r in reviews_list:
                    if not r:
                        continue
                    s = r.replace('\n', ' ').strip()
                    # use up to first 200 chars
                    snippets.append(s[:200])
                    if len(snippets) >= 3:
                        break

            # Compose ad
            headline = f"Try {product_name} — Loved by customers"
            body = " ".join(snippets) if snippets else f"Discover why customers love {product_name}."
            cta = "Buy now and enjoy the difference!"
            ad = f"{headline}\n\n{body}\n\n{cta}"
            return ad

        # Build fallback ad using reviews_text (string) or reviews list
        fallback_ad = local_generate_ad(product, reviews)
        try:
            store_ad_in_pinecone(product, fallback_ad)
        except Exception as store_exc:
            print(f"⚠️ Warning: failed to store ad in Pinecone: {store_exc}")
        return fallback_ad
