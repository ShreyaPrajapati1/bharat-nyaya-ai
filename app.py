
from flask import Flask, render_template, request, jsonify
from main import analyze_complaint
from timeline_contradiction import analyze_timeline_and_contradictions

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# API 1: AI Complaint Analysis
@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    complaint = data.get("complaint", "")

    try:
        result = analyze_complaint(complaint)
        return jsonify({
            "success": True,
            "result": result
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception:
        app.logger.exception("Complaint analysis failed")
        return jsonify({
            "success": False,
            "error": "Analysis failed. Please check the backend terminal."
        }), 500


# API 2: Timeline Analysis and Possible Contradictions
@app.route("/api/timeline-contradictions", methods=["POST"])
def timeline_contradictions():
    data = request.get_json(silent=True) or {}
    statements = data.get("statements", [])

    try:
        result = analyze_timeline_and_contradictions(statements)
        return jsonify({
            "success": True,
            "result": result
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception:
        app.logger.exception("Timeline analysis failed")
        return jsonify({
            "success": False,
            "error": "Timeline analysis failed. Please check the backend terminal."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
