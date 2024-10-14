from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the pre-trained sentiment analysis model
aspect_sentiment_model = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')

# Aspect-specific keywords for a shoe
aspects = {
    'sole': ['sole', 'grip', 'durability'],
    'toe': ['toe', 'fit', 'comfort'],
    'quality': ['quality', 'material', 'craftsmanship']
}

# Extended set of punctuation and prepositions for clause splitting
split_patterns = r'\bHowever\b|\bhowever\b|\bbut\b|\byet\b|\balthough\b|\bthough\b|\bwhile\b|\bwhereas\b|\bsince\b|\bbecause\b|,|;|:|\band\b|\bor\b|\s.\s|\?\s|!\s'

def extract_aspects(review):
    """
    Extract clauses or phrases corresponding to each aspect based on the keywords.
    """
    extracted_aspects = {aspect: [] for aspect in aspects}

    # Split the review into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', review)

    for sentence in sentences:
        clauses = re.split(split_patterns, sentence, flags=re.IGNORECASE)
        for clause in clauses:
            for aspect, keywords in aspects.items():
                if any(keyword.lower() in clause.lower() for keyword in keywords):
                    extracted_aspects[aspect].append(clause.strip())

    # Convert lists to strings for each aspect
    return {aspect: ' '.join(extracted_aspects[aspect]) for aspect in extracted_aspects if extracted_aspects[aspect]}

def analyze_sentiment(text):
    """
    Analyze sentiment using a pre-trained machine learning model.
    Returns 'positive' or 'negative' based on the majority of sentences.
    """
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    sentiments = []

    for sentence in sentences:
        result = aspect_sentiment_model(sentence)[0]
        sentiments.append(result['label'])

    # Determine final sentiment based on the majority of sentences
    return 'positive' if sentiments.count('POSITIVE') >= sentiments.count('NEGATIVE') else 'negative'

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        review = data.get('review', '')

        if not review:
            return jsonify({'status': 'error', 'message': 'Review is missing.'}), 400

        # Extract aspects from the review
        aspects_in_review = extract_aspects(review)
        sentiment_analysis = {}

        # Analyze sentiment for each aspect's sentence
        for aspect, aspect_review in aspects_in_review.items():
            if aspect_review:
                sentiment_analysis[aspect] = {
                    'review': aspect_review,
                    'sentiment': analyze_sentiment(aspect_review)
                }

        print(f"Sentiment analysis: {sentiment_analysis}")  # Debugging output
        return jsonify(sentiment_analysis)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred on the server.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
