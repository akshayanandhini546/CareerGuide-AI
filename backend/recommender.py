from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
CAREERS_FILE = ROOT / "data" / "careers.csv"

def _split(value):
    return [x.strip() for x in str(value or "").split("|") if x.strip()]

def load_careers():
    return pd.read_csv(CAREERS_FILE).fillna("")

def _profile_text(profile):
    return " ".join([
        " ".join(profile.get("skills", [])),
        " ".join(profile.get("interests", [])),
        str(profile.get("education", "")),
        str(profile.get("experience", "")),
        str(profile.get("goal", "")),
    ])

def recommend(profile, top_n=5):
    careers = load_careers()
    student_text = _profile_text(profile)
    career_texts = (
        careers["title"].astype(str) + " " +
        careers["description"].astype(str) + " " +
        careers["required_skills"].astype(str) + " " +
        careers["interests"].astype(str)
    ).tolist()

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform([student_text] + career_texts)
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    student_skills = {s.lower() for s in profile.get("skills", [])}
    results = []
    for idx, row in careers.iterrows():
        required = _split(row["required_skills"])
        missing = [s for s in required if s.lower() not in student_skills]
        results.append({
            "career_id": str(row["career_id"]),
            "title": row["title"],
            "description": row["description"],
            "match_score": round(float(scores[idx]) * 100, 1),
            "required_skills": required,
            "matched_skills": [s for s in required if s.lower() in student_skills],
            "missing_skills": missing,
            "education": row["education"],
            "projects": _split(row["project_ideas"]),
            "salary_note": row["salary_note"],
            "interests": _split(row["interests"]),
        })
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results[:max(1, min(int(top_n), len(results)))]

def make_roadmap(career_title, student_skills):
    careers = load_careers()
    match = careers[careers["title"].str.lower() == career_title.lower()]
    if match.empty:
        match = careers[careers["title"].str.lower().str.contains(career_title.lower(), regex=False)]
    if match.empty:
        return {"career": career_title, "steps": [], "message": "Career not found. Get recommendations first."}
    row = match.iloc[0]
    required = _split(row["required_skills"])
    have = {s.lower() for s in student_skills}
    missing = [s for s in required if s.lower() not in have]
    if not missing:
        missing = ["Build a portfolio project", "Practice interview questions"]
    steps = []
    for i, skill in enumerate(missing[:6], start=1):
        steps.append({
            "week": f"Week {i}",
            "topic": skill,
            "action": f"Learn {skill} fundamentals and complete one hands-on exercise.",
            "deliverable": f"A small practice task demonstrating {skill}"
        })
    steps.append({
        "week": f"Week {len(steps)+1}",
        "topic": "Portfolio and interview preparation",
        "action": "Polish two projects, update your resume, and practice explaining your work.",
        "deliverable": "Portfolio, resume and mock interview notes"
    })
    return {"career": row["title"], "steps": steps}
