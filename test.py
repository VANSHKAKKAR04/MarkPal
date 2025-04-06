from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textstat
import re
import pandas as pd

# Sample ad copies
your_ad = (
    "The King of Ketchup. Still Reigns Supreme. "
    "Image: A vibrant, close-up shot of a Heinz ketchup bottle, with a glistening, perfectly-formed ketchup swirl dripping onto a golden-brown, crinkle-cut French fry. "
    "Headline: Blind taste tests prove it: Heinz Ketchup. Unmatched. "
    "Body: For generations, Heinz Ketchup has been more than just a condiment – it's an American icon. Born in Pittsburgh, it's the ketchup that defines the perfect flavor and texture. "
    "But don't just take our word for it. We put Heinz up against the best, and the results are undeniable. "
    "In blind taste tests, experts and everyday consumers alike consistently ranked Heinz number one. Why? It's the perfect balance. "
    "The sweet tang of vinegary tomatoes, a delightful umami depth, and that signature smooth, glossy consistency that clings to your fries without ever being gloppy. "
    "It's the ketchup that elevates everything from classic burgers and hotdogs to unexpected delights (yes, even cake!). "
    "Other ketchups tried to imitate the classic taste, the perfect texture, and the signature tang—but they fell short. "
    "Some were too runny, others too sweet, and some tasted…well, let’s just say 'concerning.' "
    "Heinz delivers the uncompromising quality and taste you expect. From the iconic bottle to the unmatched flavor inside, Heinz is the ketchup that sets the standard. "
    "It's the ketchup that's been a family favorite for over 150 years, and for good reason. "
    "But don't just stop at the classic. Experience the revolutionary new Heinz Pickle Ketchup! The perfect blend of our iconic ketchup with a zesty dill pickle kick. "
    "It's the taste of that perfect McDonald's burger, but elevated. Available soon. "
    "Image: Smaller image showcasing the Heinz Pickle Ketchup bottle. "
    "Call to Action: Don't settle for second best. Grab a bottle of Heinz Ketchup – the undisputed king – today! "
    "Find it at your local grocery store. #HeinzKetchup #TheKingOfKetchup #TasteTestWinner #PerfectKetchup #HeinzPickleKetchup (coming soon!)"
)


competitor_ad = (
    "Indulge in Flavorful Perfection with Heinz Ketchup. "
    "Savor the Rich Taste of Tradition: Unleash the classic taste that has delighted taste buds for generations. "
    "Heinz Ketchup is made from sun-ripened tomatoes and a secret blend of spices, ensuring every drop is bursting with flavor. "
    "Elevate Every Bite: Whether you're dipping fries, topping a burger, or adding zing to your favorite recipes, "
    "Heinz Ketchup is the perfect accompaniment that enhances the taste of every meal. "
    "Natural Goodness in Every Squeeze: Made with only the finest ingredients and containing no artificial colors, "
    "flavors, or preservatives, you can trust Heinz Ketchup to add a dash of wholesomeness to your plate. "
    "The Must-Have Condiment: No pantry is complete without Heinz Ketchup - the iconic condiment that brings meals to life "
    "and turns every dish into a culinary masterpiece. "
    "Join the Heinz Family: Discover why families around the world have made Heinz Ketchup a staple at their table. "
    "Taste the difference, embrace the tradition, and let the deliciousness of Heinz elevate every meal. "
    "Elevate your dining experience with Heinz Ketchup - a true symbol of quality, tradition, and unbeatable flavor."
)


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