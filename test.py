from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textstat
import re
import pandas as pd

# Sample ad copies
your_ad = "Are slow apps, weak performance, and battery drain ruining your experience? The trusted iPhone 15 is here to change that. Millions have upgraded and now enjoy proven faster speeds, certified all-day battery life, and secure unmatched reliability. Powered by the proven A16 Bionic chip, even demanding tasks feel effortless, while the certified 48MP camera system captures breathtaking photos and videos with incredible clarity. Say goodbye to battery anxiety—this phone is trusted to last through your busiest days. Designed with "

competitor_ad= "The iPhone 15 ushers in a new era of innovation, blending sleek aesthetics with cutting-edge technology to deliver an unparalleled smartphone experience. Designed for creators, tech enthusiasts, and everyday users alike, this device features a revolutionary camera system that captures professtion connectivity, immersive display technology, and intelligent software optimizations, the iPhone 15 redefines what’s"

def get_readability(text):
    return textstat.flesch_reading_ease(text)

def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

def get_word_count(text):
    return len(text.split())

def get_avg_sentence_length(text):
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0
    return sum(len(s.split()) for s in sentences) / len(sentences)

def get_unique_word_ratio(text):
    words = text.split()
    return len(set(words)) / len(words) if words else 0

def contains_cta(text):
    cta_keywords = ["start", "buy", "get", "join", "try", "explore", "discover", "learn", "download"]
    return any(kw in text.lower() for kw in cta_keywords)

def contains_urgency(text):
    urgency_words = ["now", "limited", "today", "hurry", "exclusive", "instant", "fast"]
    return any(word in text.lower() for word in urgency_words)

def contains_trust_signals(text):
    trust_keywords = ["trusted", "guaranteed", "proven", "safe", "secure", "backed", "certified"]
    return any(word in text.lower() for word in trust_keywords)

def get_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    return similarity[0][0]

# Analyze both ads
def analyze_ad(ad_text):
    return {
        "Readability Score": get_readability(ad_text),
        "Sentiment Score": get_sentiment(ad_text),
        "Word Count": get_word_count(ad_text),
        "Avg Sentence Length": get_avg_sentence_length(ad_text),
        "Unique Word Ratio": get_unique_word_ratio(ad_text),
        "Has CTA": contains_cta(ad_text),
        "Has Urgency": contains_urgency(ad_text),
        "Has Trust Signals": contains_trust_signals(ad_text)
    }

your_metrics = analyze_ad(your_ad)
competitor_metrics = analyze_ad(competitor_ad)
similarity_score = get_cosine_similarity(your_ad, competitor_ad)

# Combine and present results
comparison_df = pd.DataFrame({
    "Metric": your_metrics.keys(),
    "Your Ad": your_metrics.values(),
    "Competitor Ad": competitor_metrics.values()
})

comparison_df.loc[len(comparison_df.index)] = ["Semantic Similarity", similarity_score, similarity_score]

print(comparison_df)