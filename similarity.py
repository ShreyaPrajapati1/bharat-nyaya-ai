from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_similar_cases(new_complaint, existing_cases):
    all_texts = [new_complaint] + [case["complaint"] for case in existing_cases]

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(all_texts)

    scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    results = []

    for case, score in zip(existing_cases, scores):
        results.append({
            "fir_id": case["fir_id"],
            "similarity": round(score * 100, 2),
            "complaint": case["complaint"]
        })

    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results


# Existing FIR/complaint data — temporary testing data
existing_cases = [
    {
        "fir_id": "FIR-001",
        "complaint": "Mobile phone was stolen from a market."
    },
    {
        "fir_id": "FIR-002",
        "complaint": "A wallet was stolen near a railway station."
    },
    {
        "fir_id": "FIR-003",
        "complaint": "A car was stolen from a parking area."
    }
]


# New complaint
new_complaint = "My mobile phone was stolen from the market."

results = find_similar_cases(new_complaint, existing_cases)


print("New Complaint:")
print(new_complaint)

print("\nSimilar Cases:")

for result in results:
    print(
        result["fir_id"],
        "→",
        result["similarity"],
        "% similar"
    )