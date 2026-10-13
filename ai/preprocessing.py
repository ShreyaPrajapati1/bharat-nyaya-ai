import re

def preprocess_text(text):
    # Extra spaces remove
    text = re.sub(r'\s+', ' ', text)

    # Unwanted special characters remove
    text = re.sub(r'[^\w\s.,!?]', '', text)

    # Beginning/end ke extra spaces remove
    text = text.strip()

    return text


# Test
complaint = "My   mobile phone was stolen!!!   yesterday."

processed = preprocess_text(complaint)

print("Original Complaint:")
print(complaint)

print("\nProcessed Complaint:")
print(processed)