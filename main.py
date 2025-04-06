from Models.google_search import google_search
from Models.web_scraper import scrape_website
from Models.pinecone_db import store_in_pinecone, store_ad_in_pinecone
from Models.ad_generator import generate_ad


def main():
    product_name = input("Enter product name: ")
    print(f"\n🔍 Searching for relevant websites related to '{product_name}'...")
    
    urls = google_search(product_name + " reviews")
    
    if not urls:
        print("❌ No URLs found. Exiting...")
        return
    
    print(f"✅ Found {len(urls)} URLs. Proceeding to scrape data...\n")
    
    scraped_data = []  # Store all scraped content for later use
    
    for index, url in enumerate(urls, start=1):
        print(f"🕵️ Scraping ({index}/{len(urls)}): {url}")
        content = scrape_website(url)
        
        if content:
            print(f"✅ Successfully scraped content from {url}. Storing in Pinecone...\n")
            metadata = {"url": url, "product": product_name, "content": content}
            store_in_pinecone(content, metadata)
            scraped_data.append(content)  # Collect for ad generation
        else:
            print(f"⚠️ Skipping {url} (No content extracted).")

    print("\n🚀 Data processing complete! Ready to generate ads.\n")
    
    # Generate ad only if we have scraped data
    if scraped_data:
        print("\n📝 Generating Ad...")
        ad_text = generate_ad(product_name)
        
        # Store the generated ad in Pinecone
        store_ad_in_pinecone(product_name, ad_text)
        
        print("\n📢 Generated Ad:\n", ad_text)
    else:
        print("⚠️ No scraped data found. Skipping ad generation.")

if __name__ == "__main__":
    main()
