import random

class DummyAnalytics:
    def get_impressions(self, product_name):
        return random.randint(1000, 5000)  # Simulating impressions

    def get_clicks(self, product_name):
        return random.randint(100, 500)  # Simulating clicks

    def get_unique_users(self, product_name):
        return random.randint(500, 2000)  # Simulating total users

    def get_returning_users(self, product_name):
        return random.randint(50, 500)  # Simulating returning users

    def get_ad_spend(self, product_name):
        return random.uniform(500, 5000)  # Simulating ad spend in dollars

    def get_conversions(self, product_name):
        return random.randint(10, 100)  # Simulating conversions

analytics = DummyAnalytics()

def track_ad_performance(ad_text, product_name):
    impressions = analytics.get_impressions(product_name)
    clicks = analytics.get_clicks(product_name)

    ctr = (clicks / impressions) * 100 if impressions > 0 else 0
    print(f"📊 Ad CTR for '{product_name}': {ctr:.2f}%")
    return ctr

def track_retention(product_name):
    total_users = analytics.get_unique_users(product_name)
    returning_users = analytics.get_returning_users(product_name)

    retention_rate = (returning_users / total_users) * 100 if total_users > 0 else 0
    print(f"🔄 Retention Rate for '{product_name}': {retention_rate:.2f}%")
    return retention_rate

def evaluate_ad_accuracy(generated_ad, actual_ads):
    true_positives = sum(1 for ad in actual_ads if ad in generated_ad)
    false_positives = sum(1 for ad in generated_ad if ad not in actual_ads)
    false_negatives = sum(1 for ad in actual_ads if ad not in generated_ad)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    print(f"🎯 Ad Precision: {precision:.2f}, Recall: {recall:.2f}")
    return precision, recall

def calculate_cpa(product_name):
    ad_spend = analytics.get_ad_spend(product_name)
    conversions = analytics.get_conversions(product_name)

    cpa = ad_spend / conversions if conversions > 0 else float('inf')
    print(f"💰 CPA for '{product_name}': ${cpa:.2f}")
    return cpa

# Example Usage
product_name = "Smartphone X"
generated_ad = "Buy Smartphone X – Best Features at the Best Price!"
actual_ads = ["Buy Smartphone X Now!", "Best Features of Smartphone X", "Get Smartphone X Today!"]

print("\n--- Ad Performance Metrics ---")
track_ad_performance(generated_ad, product_name)

print("\n--- User Retention Metrics ---")
track_retention(product_name)

print("\n--- Ad Accuracy Metrics ---")
evaluate_ad_accuracy(generated_ad, actual_ads)

print("\n--- Cost Per Acquisition (CPA) ---")
calculate_cpa(product_name)
