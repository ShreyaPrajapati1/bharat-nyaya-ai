from flask import Flask, request, jsonify
from flask_cors import CORS

from ai.preprocessing import preprocess_text
from language_detection import detect_language
from entity_extraction import extract_entities
from crime_classification import predict_crime_category
from summarizer import summarize_complaint

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Bharat Nyay AI API is running"
    })


@app.route("/analyze", methods=["POST"])
def analyze_complaint():

    data = request.get_json()

    if not data or "complaint" not in data:
        return jsonify({
            "error": "Complaint is required"
        }), 400

    complaint = data["complaint"]

    # 1. Preprocessing
    cleaned_text = preprocess_text(complaint)

    # 2. Language Detection
    language = detect_language(cleaned_text)

    # 3. Entity Extraction
    entities = extract_entities(cleaned_text)

    # 4. Crime Classification
    crime = predict_crime_category(cleaned_text)

    # 5. AI Summary
    summary = summarize_complaint(cleaned_text)

    return jsonify({
        "original_complaint": complaint,
        "cleaned_text": cleaned_text,
        "language": language,
        "crime_category": crime,
        "entities": entities,
        "summary": summary
    })


if __name__ == "_main_S":
    app.run(debug=True)