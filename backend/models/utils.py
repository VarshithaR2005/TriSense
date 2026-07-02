# utils.py
import re

def clean_text(text: str) -> str:
    """Simple text cleaner used across modules."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
