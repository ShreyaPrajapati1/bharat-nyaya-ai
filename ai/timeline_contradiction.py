from pathlib import Path
import zipfile, textwrap

outdir = Path("/mnt/data/timeline_contradiction_ai")
outdir.mkdir(parents=True, exist_ok=True)

module_code = r'''"""
Bharat Nyaya AI - Timeline & Possible Contradiction Analysis
-----------------------------------------------------------
Input: one or more witness/complainant statements.
Output:
  - timeline events sorted by date/time when available
  - possible conflicts where statements explicitly give different locations
    for the same person at the same normalized date and time.

IMPORTANT:
This is a heuristic aid, not a lie detector or legal conclusion.
An officer must verify every flagged item against original evidence.
"""

from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta
from typing import Any, Dict, List, Optional, Tuple

try:
    import spacy
except ImportError:
    spacy = None


# Optional spaCy model. If not installed, the module still runs but entity
# extraction is limited to dates/times and the statement text.
_NLP = None
if spacy is not None:
    for _model_name in ("en_core_web_sm", "en_core_web_md"):
        try:
            _NLP = spacy.load(_model_name)
            break
        except (OSError, IOError):
            pass


MONTHS = (
    "January|February|March|April|May|June|July|August|September|October|"
    "November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
)

DATE_PATTERNS = [
    # 5 September 2026 / September 5, 2026 / 5 Sep 2026
    re.compile(
        rf"\b(?:\d{{1,2}}\s+(?:{MONTHS})\.?,?\s+\d{{4}}|"
        rf"(?:{MONTHS})\.?\s+\d{{1,2}},?\s+\d{{4}})\b",
        re.IGNORECASE,
    ),
    # 05/09/2026, 05-09-2026, 2026-09-05
    re.compile(r"\b(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[/-]\d{1,2}[/-]\d{4})\b"),
]

TIME_PATTERN = re.compile(
    r"\b(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*(a\.?m\.?|p\.?m\.?)\b"
    r"|\b(?:at\s+)?([01]?\d|2[0-3]):([0-5]\d)\b",
    re.IGNORECASE,
)

RELATIVE_DATES = {
    "today": 0,
    "yesterday": -1,
    "tomorrow": 1,
}


def _normalise_date(raw: str, reference_date: date) -> Optional[date]:
    """Parse common English date formats without requiring another package."""
    value = raw.strip().replace(",", "")
    low = value.lower()

    if low in RELATIVE_DATES:
        return reference_date + timedelta(days=RELATIVE_DATES[low])

    formats = (
        "%d %B %Y", "%d %b %Y",
        "%B %d %Y", "%b %d %Y",
        "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y",
        "%m/%d/%Y", "%m-%d-%Y",
    )
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def _extract_date(sentence: str, reference_date: date) -> Tuple[Optional[date], Optional[str]]:
    for pattern in DATE_PATTERNS:
        match = pattern.search(sentence)
        if match:
            raw = match.group(0)
            parsed = _normalise_date(raw, reference_date)
            if parsed:
                return parsed, raw

    for word, offset in RELATIVE_DATES.items():
        if re.search(rf"\b{word}\b", sentence, re.IGNORECASE):
            return reference_date + timedelta(days=offset), word
    return None, None


def _extract_time(sentence: str) -> Tuple[Optional[str], Optional[str]]:
    match = TIME_PATTERN.search(sentence)
    if not match:
        return None, None

    raw = match.group(0).strip()
    if match.group(1) is not None:
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        meridiem = (match.group(3) or "").lower().replace(".", "")
        if hour < 1 or hour > 12 or minute > 59:
            return None, raw
        if meridiem == "pm" and hour != 12:
            hour += 12
        elif meridiem == "am" and hour == 12:
            hour = 0
    else:
        hour = int(match.group(4))
        minute = int(match.group(5))
    return f"{hour:02d}:{minute:02d}", raw


def _split_sentences(text: str) -> List[str]:
    if _NLP is not None:
        doc = _NLP(text)
        sentences = [s.text.strip() for s in doc.sents if s.text.strip()]
        if sentences:
            return sentences
    # Basic fallback sentence splitting
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+|\n+", text) if part.strip()]


def _entities(sentence: str) -> Dict[str, List[str]]:
    found: Dict[str, List[str]] = {"people": [], "locations": [], "organisations": []}
    if _NLP is None:
        return found

    try:
        doc = _NLP(sentence)
        for ent in doc.ents:
            label = ent.label_
            text = ent.text.strip()
            if not text:
                continue
            if label == "PERSON" and text not in found["people"]:
                found["people"].append(text)
            elif label in ("GPE", "LOC", "FAC") and text not in found["locations"]:
                found["locations"].append(text)
            elif label == "ORG" and text not in found["organisations"]:
                found["organisations"].append(text)
    except Exception:
        # Keep analysis running if NER fails on an unusual input.
        pass
    return found


def _extract_location(sentence: str, ner_locations: List[str]) -> Optional[str]:
    """Prefer spaCy locations; otherwise use a few common location phrases."""
    if ner_locations:
        return ner_locations[0]

    match = re.search(
        r"\b(?:in|at|near|inside|outside|from|to)\s+"
        r"([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,3})\b",
        sentence,
    )
    if match:
        candidate = match.group(1).strip()
        # Avoid treating common time/place words as locations.
        if candidate.lower() not in {"the market", "the house", "the office", "the evening"}:
            return candidate
    return None


def analyze_timeline_and_contradictions(
    statements: List[Dict[str, Any]],
    reference_date: Optional[date] = None,
) -> Dict[str, Any]:
    """
    Analyze statements.

    statements format:
      [
        {"id": "S1", "speaker": "Witness A", "text": "Ravi was in Lucknow at 8 PM on 5 September 2026."},
        {"id": "S2", "speaker": "Witness B", "text": "Ravi was in Kanpur at 8 PM on 5 September 2026."}
      ]

    reference_date: optional date used to interpret today/yesterday/tomorrow.
    """
    if not isinstance(statements, list) or not statements:
        raise ValueError("Provide at least one statement.")

    ref_date = reference_date or date.today()
    events: List[Dict[str, Any]] = []
    statement_map: Dict[str, Dict[str, Any]] = {}

    for index, item in enumerate(statements, start=1):
        if not isinstance(item, dict):
            continue
        text = str(item.get("text", "")).strip()
        if not text:
            continue

        statement_id = str(item.get("id") or f"S{index}")
        speaker = str(item.get("speaker") or "Unknown")
        statement_map[statement_id] = {
            "id": statement_id,
            "speaker": speaker,
            "text": text,
        }

        for sentence in _split_sentences(text):
            parsed_date, raw_date = _extract_date(sentence, ref_date)
            parsed_time, raw_time = _extract_time(sentence)
            ents = _entities(sentence)
            location = _extract_location(sentence, ents["locations"])

            # Keep sentences that contain temporal information or a useful place/person.
            if not (parsed_date or parsed_time or location or ents["people"]):
                continue

            events.append({
                "statement_id": statement_id,
                "speaker": speaker,
                "date": parsed_date.isoformat() if parsed_date else None,
                "date_text": raw_date,
                "time": parsed_time,
                "time_text": raw_time,
                "people": ents["people"],
                "location": location,
                "organisations": ents["organisations"],
                "event_text": sentence,
                "needs_review": not bool(parsed_date and parsed_time),
            })

    # Chronological ordering: known dates/times first; undated items after.
    def sort_key(event: Dict[str, Any]) -> Tuple[int, str, str, str]:
        date_value = event.get("date") or "9999-99-99"
        time_value = event.get("time") or "99:99"
        return (0 if event.get("date") else 1, date_value, time_value, event["statement_id"])

    events.sort(key=sort_key)

    # Only flag clear, explicit conflicts: same person, same explicit date/time,
    # different explicit locations, from different statements.
    conflicts: List[Dict[str, Any]] = []
    for i, first in enumerate(events):
        if not first.get("date") or not first.get("time") or not first.get("location"):
            continue
        for second in events[i + 1:]:
            if second["statement_id"] == first["statement_id"]:
                continue
            if (
                second.get("date") != first.get("date")
                or second.get("time") != first.get("time")
                or not second.get("location")
                or first["location"].casefold() == second["location"].casefold()
            ):
                continue

            people_a = {p.casefold() for p in first.get("people", [])}
            people_b = {p.casefold() for p in second.get("people", [])}
            shared_people = sorted(people_a & people_b)

            # If both statements identify people but have no person in common,
            # do not infer that they refer to the same person.
            if people_a and people_b and not shared_people:
                continue

            conflicts.append({
                "type": "different_locations_at_same_time",
                "severity": "review",
                "statement_ids": [first["statement_id"], second["statement_id"]],
                "date": first["date"],
                "time": first["time"],
                "people_in_common": shared_people,
                "location_1": first["location"],
                "location_2": second["location"],
                "statement_1": first["event_text"],
                "statement_2": second["event_text"],
                "explanation": (
                    "These statements mention different locations for the same "
                    "explicit date and time. Verify identities, time accuracy, "
                    "travel possibility, and the original statements."
                ),
            })

    return {
        "reference_date": ref_date.isoformat(),
        "timeline": events,
        "possible_contradictions": conflicts,
        "notes": [
            "This tool flags possible inconsistencies; it does not determine truth or guilt.",
            "Relative dates such as 'yesterday' use the reference date supplied to this function, or the computer's current date.",
            "Events without explicit date and time may be incomplete and need human review.",
            "spaCy NER is statistical and may miss or mislabel people and locations.",
        ],
    }


if __name__ == "__main__":
    demo_statements = [
        {
            "id": "S1",
            "speaker": "Witness A",
            "text": "Ravi was in Lucknow at 8 PM on 5 September 2026.",
        },
        {
            "id": "S2",
            "speaker": "Witness B",
            "text": "Ravi was in Kanpur at 8 PM on 5 September 2026.",
        },
        {
            "id": "S3",
            "speaker": "Complainant",
            "text": "My phone was stolen yesterday at 7 PM in Lucknow.",
        },
    ]
    result = analyze_timeline_and_contradictions(demo_statements)
    print("\nTIMELINE")
    for event in result["timeline"]:
        print(event)
    print("\nPOSSIBLE CONTRADICTIONS")
    for conflict in result["possible_contradictions"]:
        print(conflict)
    if not result["possible_contradictions"]:
        print("No clear location/time conflict detected.")
'''
(outdir / "timeline_contradiction.py").write_text(module_code, encoding="utf-8")

requirements = """# Core dependency for named-entity extraction (people/places)
spacy>=3.7,<4
"""
(outdir / "requirements-ai.txt").write_text(requirements, encoding="utf-8")

readme = r'''# Bharat Nyaya AI: Timeline & Possible Contradiction Module

## 1. Install
In the same Python environment as your Flask app:
```powershell
python -m pip install -r requirements-ai.txt
python -m spacy download en_core_web_sm
```

If you do not want spaCy entities yet, the module can still run without spaCy, but people/place extraction will be more limited.

## 2. Copy
Copy `timeline_contradiction.py` into the root of your project, next to `app.py` and `main.py`.

## 3. Run standalone demo
```powershell
python timeline_contradiction.py
```

## 4. Call it from Python
```python
from timeline_contradiction import analyze_timeline_and_contradictions

statements = [
    {"id": "S1", "speaker": "Witness A",
     "text": "Ravi was in Lucknow at 8 PM on 5 September 2026."},
    {"id": "S2", "speaker": "Witness B",
     "text": "Ravi was in Kanpur at 8 PM on 5 September 2026."},
]
result = analyze_timeline_and_contradictions(statements)
print(result["timeline"])
print(result["possible_contradictions"])
```

## 5. Flask endpoint (optional)
Add this to `app.py`, below your existing routes:
```python
from timeline_contradiction import analyze_timeline_and_contradictions

@app.route("/api/timeline-contradictions", methods=["POST"])
def timeline_contradictions():
    data = request.get_json(silent=True) or {}
    statements = data.get("statements", [])
    try:
        result = analyze_timeline_and_contradictions(statements)
        return jsonify({"success": True, "result": result})
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400
```

Example request body:
```json
{
  "statements": [
    {"id": "S1", "speaker": "Witness A", "text": "Ravi was in Lucknow at 8 PM on 5 September 2026."},
    {"id": "S2", "speaker": "Witness B", "text": "Ravi was in Kanpur at 8 PM on 5 September 2026."}
  ]
}
```

## Important limitations
- The current contradiction rule is deliberately conservative: it flags different explicit locations only when date and time match and the statements are from different sources.
- It does not yet detect all kinds of contradictions (e.g., different actions, quantities, identity disputes, vague time ranges, or implied contradictions).
- Names and locations extracted by spaCy are probabilistic and should be reviewed.
- Do not use this output as proof that a witness lied. A human investigator must verify the original statements and other evidence.
'''
(outdir / "README_SETUP.md").write_text(readme, encoding="utf-8")

zip_path = Path("/mnt/data/timeline_contradiction_ai.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in outdir.iterdir():
        zf.write(p, arcname=p.name)

print("Created files:")
for p in sorted(outdir.iterdir()):
    print(f"- {p} ({p.stat().st_size} bytes)")
print(f"ZIP: {zip_path} ({zip_path.stat().st_size} bytes)")
