// script.js
const API_URL = "http://127.0.0.1:5000/analyze";

document.getElementById("analyzeBtn").addEventListener("click", analyze);

async function analyze() {
  const headline = document.getElementById("headline").value.trim();
  const article = document.getElementById("article").value.trim();
  const output = document.getElementById("output");
  output.innerHTML = "<p>Analyzing... please wait (models may load on first run)</p>";

  if (!headline || !article) {
    output.innerHTML = "<p style='color:#c00'>Please enter both headline and article.</p>";
    return;
  }

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ headline, article })
    });

    if (!res.ok) {
      const txt = await res.text();
      output.innerHTML = `<p style='color:#c00'>Server error: ${res.status} ${txt}</p>`;
      return;
    }

    const data = await res.json();
    renderResult(data);
  } catch (err) {
    output.innerHTML = `<p style='color:#c00'>Network error: ${err.message}</p>`;
  }
}

function renderResult(data) {
  const output = document.getElementById("output");
  if (data.error) {
    output.innerHTML = `<p style='color:#c00'>Error: ${data.error}</p>`;
    return;
  }

  // Label color
  let labelClass = "label-genuine";
  if (data.label === "Possibly Misleading") labelClass = "label-possible";
  if (data.label === "Highly Suspicious") labelClass = "label-high";

  output.innerHTML = `
    <h3>Decision: <span class="label-chip ${labelClass}">${data.label}</span></h3>
    <div class="result-row"><b>Final Score:</b> ${data.final_score}</div>
    <div class="result-row"><b>Similarity (0..1):</b> ${data.similarity}  &nbsp; <small>(similarity_misleading: ${data.similarity_misleading})</small></div>
    <div class="result-row"><b>Emotion:</b> headline ${data.headline_sentiment} &nbsp; article ${data.article_sentiment} &nbsp; <small>(difference: ${data.emotion_difference})</small></div>
    <div class="result-row"><b>Category:</b> headline = ${data.headline_category} (${data.category_confidence_headline}), article = ${data.article_category} (${data.category_confidence_article})  &nbsp; <small>(mismatch: ${data.category_mismatch})</small></div>
    <hr/>
    <div><small>Note: Scores are probabilistic indicators. Use for demo and research only.</small></div>
  `;
}
