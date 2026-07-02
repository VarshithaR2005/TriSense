# emotion.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_emotion_score(headline: str, article: str) -> dict:
    """
    Returns headline and article compound sentiment and their difference.
    compound ∈ [-1,1]. Difference = headline - article
    """
    if not isinstance(headline, str):
        headline = ""
    if not isinstance(article, str):
        article = ""
    h = analyzer.polarity_scores(headline).get("compound", 0.0)
    a = analyzer.polarity_scores(article).get("compound", 0.0)
    diff = h - a
    return {
        "headline_sentiment": float(h),
        "article_sentiment": float(a),
        "emotion_difference": float(diff)
    }
