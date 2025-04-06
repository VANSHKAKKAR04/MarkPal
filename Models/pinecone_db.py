from config import (
    PINECONE_API_KEY, 
    PINECONE_INDEX_NAME, 
    PINECONE_ADS_INDEX_NAME
)
from Models.embedding import get_embedding
from pinecone import Pinecone

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Initialize indexes
index = pc.Index(name=PINECONE_INDEX_NAME)
ads_index = pc.Index(name=PINECONE_ADS_INDEX_NAME)

def store_in_pinecone(text, metadata):
    """Stores text embeddings in Pinecone."""
    embedding = get_embedding(text)
    index.upsert(vectors=[{"id": metadata["url"], "values": embedding, "metadata": metadata}])

def query_pinecone(query, top_k=3):
    """Queries Pinecone to retrieve the most relevant stored embeddings."""
    query_embedding = get_embedding(query)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return [res["metadata"]["content"] for res in results.get("matches", [])]

def store_ad_in_pinecone(product, ad_text):
    """Stores generated ad content in a separate Pinecone index."""
    embedding = get_embedding(ad_text)
    metadata = {"product": product, "ad_text": ad_text}
    ads_index.upsert(vectors=[{"id": product, "values": embedding, "metadata": metadata}])

def query_ad_pinecone(product, top_k=1):
    """Retrieves stored ads for a product from Pinecone."""
    query_embedding = get_embedding(product)
    results = ads_index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return [res["metadata"]["ad_text"] for res in results.get("matches", [])]
