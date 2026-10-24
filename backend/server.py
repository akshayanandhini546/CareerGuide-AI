from pathlib import Path
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from backend.recommender import load_careers, recommend, make_roadmap
from backend.storage import save_profile, get_profile, save_recommendations
from backend.assistant import answer_question

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

app = Flask(__name__)
CORS(app)

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "CareerGuide AI API"})

@app.get("/api/careers")
def careers():
    df = load_careers()
    return jsonify(df.to_dict(orient="records"))

@app.post("/api/recommend")
def api_recommend():
    payload = request.get_json(silent=True) or {}
    if not payload.get("skills") and not payload.get("interests"):
        return jsonify({"error": "Please provide at least one skill or interest."}), 400
    results = recommend(payload, payload.get("top_n", 5))
    student_id = payload.get("student_id")
    if student_id:
        save_recommendations(student_id, results)
    return jsonify({"recommendations": results})

@app.post("/api/roadmap")
def roadmap():
    payload = request.get_json(silent=True) or {}
    if not payload.get("career"):
        return jsonify({"error": "career is required"}), 400
    return jsonify(make_roadmap(payload["career"], payload.get("skills", [])))

@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    if not payload.get("message", "").strip():
        return jsonify({"error": "message is required"}), 400
    return jsonify({"answer": answer_question(payload["message"], payload.get("profile", {}))})

@app.post("/api/profile")
def profile_save():
    payload = request.get_json(silent=True) or {}
    if not payload.get("student_id"):
        return jsonify({"error": "student_id is required"}), 400
    return jsonify({"profile": save_profile(payload)})

@app.get("/api/profile/<student_id>")
def profile_get(student_id):
    profile = get_profile(student_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify({"profile": profile})

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)
