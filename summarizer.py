def summarize_complaint(text):
    # Complaint ko sentences mein divide karna
    sentences = text.split(".")

    # Empty sentences remove karna
    sentences = [s.strip() for s in sentences if s.strip()]

    # Prototype: important sentences ko select karna
    keywords = [
        "stolen", "theft", "robbed", "fraud",
        "attack", "threat", "missing",
        "चोरी", "धोखा", "हमला", "धमकी"
    ]

    important_sentences = []

    for sentence in sentences:
        if any(word in sentence.lower() for word in keywords):
            important_sentences.append(sentence)

    # Agar important sentence nahi mila
    if not important_sentences:
        important_sentences = sentences[:2]

    return ". ".join(important_sentences) + "."


# Test complaint
complaint = """
Rahul went to the market in Lucknow on 5 September 2026.
He visited several shops during the evening.
His mobile phone was stolen while he was in the market.
He noticed that the phone was missing after some time.
He wants to report the incident.
"""

summary = summarize_complaint(complaint)

print("Original Complaint:")
print(complaint)

print("\nAI Summary:")
print(summary)