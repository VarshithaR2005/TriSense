# similarity.py
from sentence_transformers import SentenceTransformer, util

# lightweight SBERT model (fast on CPU)
_MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(_MODEL_NAME)

def get_similarity(headline: str, article: str) -> float:
    """
    Returns cosine similarity in [0,1] between headline and article.
    Higher = more similar.
    """
    if not headline:
        headline = ""
    if not article:
        article = ""
    h_emb = model.encode(headline, convert_to_tensor=True)
    a_emb = model.encode(article, convert_to_tensor=True)
    score = util.cos_sim(h_emb, a_emb).item()  # typically in [-1,1]
    # Clamp & map to [0,1] (some models give negative rarely)
    score = max(-1.0, min(1.0, score))
    normalized = (score + 1.0) / 2.0
    return float(normalized)
