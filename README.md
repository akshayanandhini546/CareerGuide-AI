# CareerGuide AI — Full-Stack Personalized Career Recommendation Agent

A student-focused career recommendation project based on the supplied abstract.

## Features
- Streamlit dashboard and student profile form
- Flask REST API backend
- Scikit-learn TF-IDF + cosine-similarity career matching
- Career recommendations with match scores and missing skills
- Personalized learning roadmap and course/project suggestions
- Internship/job suggestions from a small sample dataset
- Career Q&A assistant with a rule-based fallback
- Optional MongoDB persistence; app works without MongoDB using local JSON storage

> Dataset note: `data/careers.csv`, `data/courses.csv`, and `data/opportunities.csv` are demonstration datasets created for this project. They are not live job listings or an externally verified labor-market dataset.

## Tech stack
- Frontend: Streamlit
- Backend: Flask
- ML: scikit-learn, pandas
- Database: MongoDB (optional) or local JSON fallback
- Charts: Plotly

## Project structure
```text
CareerGuide_AI_FullStack/
├── app.py                    # Streamlit frontend
├── backend/
│   ├── __init__.py
│   ├── server.py             # Flask API
│   ├── recommender.py        # ML matching + skill gap
│   ├── storage.py             # MongoDB/local JSON storage
│   └── assistant.py           # Career Q&A fallback
├── data/
│   ├── careers.csv
│   ├── courses.csv
│   └── opportunities.csv
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup (Windows / VS Code)

### 1. Create and activate a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install packages
```powershell
pip install -r requirements.txt
```

### 3. Start the Flask backend
Open Terminal 1 in the project folder:
```powershell
python -m backend.server
```
Backend runs at `http://127.0.0.1:5000`.

### 4. Start the Streamlit frontend
Open Terminal 2 in the same folder:
```powershell
streamlit run app.py
```
Streamlit opens in your browser, usually at `http://localhost:8501`.

## Optional MongoDB
By default, the project saves profiles/results to `data/local_store.json`.
To use MongoDB:
1. Install and run MongoDB locally or create a MongoDB Atlas database.
2. Copy `.env.example` to `.env`.
3. Set `MONGODB_URI` and `MONGODB_DB`.
4. Restart the Flask backend.

## API endpoints
- `GET /api/health` — backend status
- `GET /api/careers` — list careers
- `POST /api/recommend` — rank careers and identify skill gaps
- `POST /api/roadmap` — create a roadmap for a selected career
- `POST /api/chat` — career Q&A assistant
- `POST /api/profile` — save a student profile
- `GET /api/profile/<student_id>` — retrieve saved profile

### Example request
```json
{
  "name": "Student",
  "education": "B.Tech IT",
  "skills": ["Python", "SQL", "HTML", "CSS"],
  "interests": ["Web Development", "Problem Solving"],
  "experience": "Beginner",
  "goal": "Get an internship"
}
```

## How the recommendation works
1. Student skills, interests, education, experience and goal are converted into a profile text.
2. TF-IDF vectorization represents the student and career descriptions.
3. Cosine similarity ranks career profiles by textual match.
4. Skill-gap analysis compares the student's selected skills with each career's expected skills.
5. The roadmap suggests a sequence of learning topics, practice projects and relevant courses.

The score is a similarity-based estimate for educational guidance, not a guarantee of employability. Students should verify course details and opportunities independently.

## Troubleshooting
- If the Streamlit page says the backend is unavailable, ensure Terminal 1 is running `python -m backend.server`.
- If port 5000 is occupied, change `API_URL` in `app.py` and `PORT` in `backend/server.py`.
- MongoDB is optional; the app can run without it.
