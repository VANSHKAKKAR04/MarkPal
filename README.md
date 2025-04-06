# MarkPal: AI-Powered Marketing Assistant

MarkPal is an AI-powered marketing assistant that automates product research, web scraping, and ad generation using cutting-edge NLP models. It helps businesses create compelling advertisements based on real-time customer reviews and market trends.

## 🚀 Features

- **Web Scraping:** Gathers product reviews and insights from e-commerce platforms.
- **Ad Generation:** Leverages Google Gemini AI to generate compelling ad content.
- **Pinecone Vector Store:** Handles storage and retrieval of embeddings for ads and reviews.
- **Google Search API:** Collects real-time top search results for keyword enrichment.
- **Modular Pipeline:** Organized and extendable structure for each ML/NLP component.
- **Evaluation Notebooks:** Research notebooks for performance analysis and benchmarking.

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/VANSHKAKKAR04/MarkPal.git
cd MarkPal
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File

Add your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
PINECONE_INDEX_NAME=your_index_name
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CX_ID=your_google_cx_id
```

## 📁 Project Structure

```
MarkPal/
│
├── Dataset/
│   └── db.txt                      # Sample scraped data or embeddings
│
├── app/
│   ├── ad_generator.py             # AI ad content generation logic
│   ├── config.py                   # Loads env variables and configurations
│   ├── embedding.py                # Converts text to embeddings
│   ├── google_search.py            # Handles Google Custom Search API
│   ├── main.py                     # Main orchestrator for the pipeline
│   ├── pinecone_db.py              # Vector DB interactions
│   ├── web_scraper.py              # Scrapes reviews from websites
|
├── models/                     
|    ├── config.py                       # Optional central config (legacy or shared)
|    ├── evaluate.ipynb                  # Evaluation and analysis notebook
|    ├── model.ipynb                     # Model training/development notebook
├── test.py                         # Test script for end-to-end pipeline
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation
```

## ▶️ Usage

```bash
python app/main.py
```

Enter a product name when prompted. The pipeline will handle scraping, embedding, searching, and generating an ad.

## 📌 Notebooks

- `model.ipynb`: Develop and test model-based ad generation.
- `evaluate.ipynb`: Analyze performance of generated content and embeddings.

## 💡 Future Enhancements

- Multilingual support for ad generation.
- Social media integration for direct publishing.
- Dashboard for managing campaigns and analytics.
- Feedback loop from ad performance.

## 🤝 Contributing

Feel free to fork the repo and open a pull request with improvements or issues.

## 📄 License

Licensed under the [MIT License](LICENSE).
