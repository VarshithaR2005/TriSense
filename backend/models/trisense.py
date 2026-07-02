# trisense.py
from .similarity import get_similarity
from .emotion import get_emotion_score
from .category import category_mismatch

def trisense_score(headline: str, article: str,
                   weights=(0.5, 0.3, 0.2),
                   thresholds=(0.3, 0.6)) -> dict:
    """
    Combine similarity, emotion and category signals into final TriSense score & label.
    Returns a detailed dictionary of component scores and the final decision.
    """

    # 1) Similarity (higher -> more similar). Convert to 'misleading' measure
    sim = get_similarity(headline, article)      # 0..1 (high = similar)
    sim_mis = 1.0 - sim                          # 0..1 (high = more misleading)

    # 2) Emotion exaggeration
    emo = get_emotion_score(headline, article)
    diff = emo.get("emotion_difference", 0.0)    # can be negative..positive
    # Normalize emotion difference to [0,1] (simple mapping)
    # diff range roughly [-2,2] theoretically; we map (-1 -> 0) (0 -> 0.5) (1 ->1)
    emo_norm = max(0.0, min(1.0, (diff + 1.0) / 2.0))

    # 3) Category mismatch (0 or 1)
    cat = category_mismatch(headline, article)
    cat_score = float(cat.get("mismatch_score", 0.0))

    # 4) Weighted fusion
    w_sim, w_emo, w_cat = weights
    final = (w_sim * sim_mis) + (w_emo * emo_norm) + (w_cat * cat_score)
    final = float(max(0.0, min(1.0, final)))

    # 5) Labeling
    t_low, t_high = thresholds
    if final <= t_low:
        label = "Genuine"
    elif final <= t_high:
        label = "Possibly Misleading"
    else:
        label = "Highly Suspicious"

    return {
        "similarity": round(sim, 3),
        "similarity_misleading": round(sim_mis, 3),
        "headline_sentiment": round(emo.get("headline_sentiment", 0.0), 3),
        "article_sentiment": round(emo.get("article_sentiment", 0.0), 3),
        "emotion_difference": round(diff, 3),
        "emotion_normalized": round(emo_norm, 3),
        "headline_category": cat.get("headline_category"),
        "article_category": cat.get("article_category"),
        "category_confidence_headline": round(cat.get("headline_confidence", 0.0), 3),
        "category_confidence_article": round(cat.get("article_confidence", 0.0), 3),
        "category_mismatch": int(cat_score),
        "final_score": round(final, 3),
        "label": label
    }
