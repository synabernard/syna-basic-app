from flask import Flask, request, render_template_string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Multi-Sentence Sentiment Analyzer</title>
  <style>
    body { font-family: Arial; text-align:center; margin-top:40px; background:#f6f8fa; }
    textarea { width:60%; height:150px; font-size:16px; }
    button { padding:10px 20px; font-size:16px; margin-top:10px; }
    .positive { color:green; }
    .negative { color:red; }
    .neutral { color:orange; }
    .summary { margin-top:20px; font-weight:bold; }
  </style>
</head>
<body>
  <h1> Sentiment Analyzer</h1>
  <p>Enter multiple sentences below (each on a new line):</p>
  <form method="POST">
    <textarea name="text" placeholder="Type here..."></textarea><br>
    <button type="submit">Analyze</button>
  </form>

  {% if results %}
  <h2>Results</h2>
  {% for r in results %}
    <p class="{{r[1]|lower}}">{{r[0]}} → {{r[1]}} (score = {{r[2]}})</p>
  {% endfor %}
  <div class="summary">
    <p style="color:green;">Most positive: {{best}}</p>
    <p style="color:red;">Most negative: {{worst}}</p>
  </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    results, best, worst = None, None, None
    if request.method == "POST":
        text = request.form["text"]
        sentences = [s.strip() for s in text.split("\n") if s.strip()]
        if sentences:
            best = {"text": None, "score": -1}
            worst = {"text": None, "score": 1}
            results = []
            for s in sentences:
                score = analyzer.polarity_scores(s)['compound']
                sentiment = "Positive" if score >= 0.05 else "Negative" if score <= -0.05 else "Neutral"
                results.append((s, sentiment, round(score, 2)))
                if score > best["score"]:
                    best = {"text": s, "score": score}
                if score < worst["score"]:
                    worst = {"text": s, "score": score}
            best = best["text"]
            worst = worst["text"]
    return render_template_string(HTML, results=results, best=best, worst=worst)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
