import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "type": ent.label_
        })

    return entities


# Test complaint
complaint = "Rahul's mobile phone was stolen in Lucknow on 5 September 2026."

result = extract_entities(complaint)

print("Extracted Entities:")

for entity in result:
    print(entity["type"], ":", entity["text"])