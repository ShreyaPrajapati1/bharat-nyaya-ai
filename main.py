
from ai.preprocessing import preprocess_text
from language_detection import detect_language
from entity_extraction import extract_entities
from crime_classification import predict_crime_category
from summarizer import summarize_complaint
from similarity import find_similar_cases


def analyze_complaint(complaint):
    """
    Analyze a complaint using the existing AI modules.
    This function can be called by Flask or from the terminal.
    """

    if not isinstance(complaint, str) or not complaint.strip():
        raise ValueError("Please enter a valid complaint.")

    # 1. Preprocess complaint
    cleaned_text = preprocess_text(complaint.strip())

    # 2. Detect language
    language = detect_language(cleaned_text)

    # 3. Extract entities
    entities = extract_entities(cleaned_text)

    # 4. Predict crime category
    crime = predict_crime_category(cleaned_text)

    # 5. Generate complaint summary
    summary = summarize_complaint(cleaned_text)

    # 6. Find similar cases
    # This assumes find_similar_cases accepts complaint text.
    # Adjust the call if your similarity.py uses a different signature.
    try:
        similar_cases = find_similar_cases(cleaned_text)
    except TypeError:
        similar_cases = []

    # Return results for Flask API / frontend
    return {
        "original_complaint": complaint,
        "cleaned_text": cleaned_text,
        "language": language,
        "crime_category": crime,
        "entities": entities,
        "summary": summary,
        "similar_cases": similar_cases
    }


# Run this section only when executing main.py directly.
# Importing analyze_complaint from Flask will not ask for terminal input.
if __name__ == "__main__":
    print("========================================")
    print(" BHARAT NYAYA AI - COMPLAINT ANALYSIS")
    print("========================================")

    complaint = input("\nEnter your complaint: ")

    try:
        result = analyze_complaint(complaint)

        print("\n========== AI ANALYSIS ==========")
        print("Language:", result["language"])
        print("Crime Category:", result["crime_category"])

        print("\nExtracted Entities:")
        if result["entities"]:
            for entity in result["entities"]:
                print(
                    entity.get("type", "Entity"),
                    ":",
                    entity.get("text", "")
                )
        else:
            print("No entities detected.")

        print("\nComplaint Summary:")
        print(result["summary"])

        print("\nSimilar Cases:")
        if result["similar_cases"]:
            for case in result["similar_cases"]:
                print(case)
        else:
            print("No similar cases returned.")

    except ValueError as error:
        print("Input Error:", error)

    except Exception as error:
        print("Analysis Error:", error)
