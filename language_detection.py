def detect_language(text):
    # Hindi Unicode range: \u0900-\u097F
    hindi_characters = 0
    english_characters = 0

    for char in text:
        if '\u0900' <= char <= '\u097F':
            hindi_characters += 1
        elif char.isalpha():
            english_characters += 1

    if hindi_characters > english_characters:
        return "Hindi"
    elif english_characters > 0:
        return "English"
    else:
        return "Unknown"


# Test complaints
complaint1 = "My mobile phone was stolen yesterday."
complaint2 = "मेरा मोबाइल फोन कल चोरी हो गया।"

print("Complaint 1 Language:", detect_language(complaint1))
print("Complaint 2 Language:", detect_language(complaint2))