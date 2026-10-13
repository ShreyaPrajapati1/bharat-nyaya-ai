from datetime import datetime
import re

def analyze_timeline_and_contradictions(statements, reference_date=None):
    if not isinstance(statements, list) or not statements:
        raise ValueError("Please provide a non-empty list of statements.")

    events = []
    for item in statements:
        if not isinstance(item, dict) or not item.get("text", "").strip():
            continue

        text = item["text"].strip()
        dates = re.findall(
            r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
            text,
            re.IGNORECASE
        )
        times = re.findall(r"\b\d{1,2}(?::\d{2})?\s*(?:AM|PM)\b", text, re.IGNORECASE)
        locations = re.findall(r"\b(?:in|at|near)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)", text)

        events.append({
            "id": item.get("id", f"S{len(events) + 1}"),
            "speaker": item.get("speaker", "Unknown"),
            "statement": text,
            "dates_found": dates,
            "times_found": times,
            "locations_found": locations
        })

    conflicts = []
    for i, first in enumerate(events):
        for second in events[i + 1:]:
            same_date = set(first["dates_found"]) & set(second["dates_found"])
            same_time = set(t.lower() for t in first["times_found"]) & set(t.lower() for t in second["times_found"])
            loc1 = {x.lower() for x in first["locations_found"]}
            loc2 = {x.lower() for x in second["locations_found"]}

            if same_date and same_time and loc1 and loc2 and loc1.isdisjoint(loc2):
                conflicts.append({
                    "statement_1": first["id"],
                    "statement_2": second["id"],
                    "date": list(same_date)[0],
                    "time": list(same_time)[0],
                    "location_1": first["locations_found"],
                    "location_2": second["locations_found"],
                    "note": "Possible location inconsistency. Human review required."
                })

    return {
        "timeline": events,
        "possible_contradictions": conflicts,
        "disclaimer": "AI flags are preliminary and do not establish that any person is lying."
    }


if __name__ == "__main__":
    demo = [
        {"id": "S1", "speaker": "Witness A", "text": "Ravi was in Lucknow at 8 PM on 5 September 2026."},
        {"id": "S2", "speaker": "Witness B", "text": "Ravi was in Kanpur at 8 PM on 5 September 2026."}
    ]
    import json
    print(json.dumps(analyze_timeline_and_contradictions(demo), indent=2))
