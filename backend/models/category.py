# category.py
from transformers import pipeline

# Zero-shot classification pipeline (no training needed)
_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

CATEGORIES = [
    "politics", "sports", "technology", "science",
    "health", "entertainment", "business", "world news",
    "crime", "education"
]

def category_mismatch(headline: str, article: str) -> dict:
    """
    Predict categories for headline and article using zero-shot classification.
    Returns predicted labels, confidences and mismatch score (0 or 1).
    """
    if not isinstance(headline, str) or headline.strip() == "":
        h_res = {"labels": ["unknown"], "scores": [0.0]}
    else:
        h_res = _classifier(headline, CATEGORIES)
    if not isinstance(article, str) or article.strip() == "":
        a_res = {"labels": ["unknown"], "scores": [0.0]}
    else:
        a_res = _classifier(article, CATEGORIES)

    h_label = h_res['labels'][0]
    a_label = a_res['labels'][0]
    h_score = float(h_res['scores'][0]) if h_res['scores'] else 0.0
    a_score = float(a_res['scores'][0]) if a_res['scores'] else 0.0
    mismatch = 0 if h_label == a_label else 1

    return {
        "headline_category": h_label,
        "article_category": a_label,
        "headline_confidence": h_score,
        "article_confidence": a_score,
        "mismatch_score": mismatch
    }
