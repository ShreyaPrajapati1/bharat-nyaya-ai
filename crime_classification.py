def predict_crime_category(text):
    text = text.lower()

    if any(word in text for word in ["stolen", "theft", "robbed", "चोरी"]):
        return "Theft"

    elif any(word in text for word in ["hit", "attack", " मार", "हमला"]):
        return "Assault"

    elif any(word in text for word in ["threat", " धमकी"]):
        return "Criminal Intimidation"

    elif any(word in text for word in ["fraud", "scam", " धोखा"]):
        return "Fraud"

    else:
        return "Other / Unknown"


# Test
complaint = "My mobile phone was stolen from the market."

category = predict_crime_category(complaint)

print("Complaint:", complaint)
print("Suggested Crime Category:", category)