```python
from flask import Flask
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import nltk
from pathlib import Path

app = Flask("Sentiment Analyzer")

# Configure the local NLTK data directory
BASE_DIR = Path(__file__).resolve().parent
nltk.data.path.insert(0, str(BASE_DIR))

# Initialize VADER Sentiment Analyzer
sia = SentimentIntensityAnalyzer()


@app.get('/')
def home():
    return (
        "Welcome to the Sentiment Analyzer. "
        "Use /analyze/text to get the sentiment"
    )


@app.get('/analyze/<input_txt>')
def analyze_sentiment(input_txt):

    # Calculate sentiment scores
    scores = sia.polarity_scores(input_txt)

    pos = float(scores['pos'])
    neg = float(scores['neg'])
    neu = float(scores['neu'])

    # Determine sentiment
    result = "positive"

    if neg > pos and neg > neu:
        result = "negative"
    elif neu > neg and neu > pos:
        result = "neutral"

    return json.dumps({"sentiment": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
```
