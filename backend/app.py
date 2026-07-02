# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from models.trisense import trisense_score

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from frontend served elsewhere

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "TriSense backend running"})

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    headline = data.get("headline", "")
    article = data.get("article", "")

    # Basic input checks
    if not isinstance(headline, str) or not isinstance(article, str):
        return jsonify({"error": "headline and article must be strings"}), 400

    result = trisense_score(headline, article)
    return jsonify(result), 200

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
