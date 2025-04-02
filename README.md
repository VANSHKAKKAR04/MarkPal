# MarkPal: AI-Powered Marketing Assistant

MarkPal is an AI-powered marketing assistant that automates product research, web scraping, and ad generation using cutting-edge NLP models. It helps businesses create compelling advertisements based on real-time customer reviews and market trends.

## 🚀 Features
- **Web Scraping:** Extracts product reviews and insights from relevant websites.
- **AI-Powered Ad Generation:** Uses Google Gemini AI to create engaging advertisements.
- **Pinecone Vector Database:** Stores and retrieves product reviews and generated ad content.
- **Custom Search Integration:** Fetches top search results using Google Custom Search API.
- **Scalability:** Designed for efficient data processing and marketing automation.

## 🛠️ Installation

### 1. Clone the Repository
```bash
 git clone https://github.com/VANSHKAKKAR04/MarkPal.git
 cd MarkPal
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys
Create a `.env` file and add the following keys:
```
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
PINECONE_INDEX_NAME=your_index_name
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CX_ID=your_google_cx_id
```

## 📌 Project Structure
```
MarkPal/
│── database/
│   ├── pinecone_db.py  # Handles Pinecone interactions
│── embeddings/
│   ├── embedding.py  # Generates vector embeddings
│── generator/
│   ├── ad_generator.py  # AI-generated ad content
│── scraper/
│   ├── web_scraper.py  # Web scraping logic
│── search/
│   ├── google_search.py  # Fetches search results
│── main.py  # Entry point for running the application
│── config.py  # API keys and configurations
│── requirements.txt  # List of dependencies
│── README.md  # Documentation
```

## 🚀 Usage
Run the application using:
```bash
python main.py
```
Follow the prompts to enter a product name, scrape reviews, and generate AI-powered advertisements.

## 🔥 Future Improvements
- ✅ Advanced sentiment analysis for better ad targeting.
- ✅ Multilingual ad generation support.
- ✅ Social media post automation.
- ✅ Integration with more databases for scalable storage.

## 🤝 Contributing
Contributions are welcome! Feel free to submit a PR or open an issue for improvements.

## 📜 License
This project is licensed under the [MIT License](LICENSE).

