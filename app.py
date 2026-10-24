
import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Career Compass AI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv(
    "CAREERGUIDE_API_URL",
    "http://127.0.0.1:5000/api"
)

# -------------------- DESIGN --------------------

st.markdown("""
<style>
.stApp {
    background: #f3f6fc;
    color: #163452;
}

[data-testid="stHeader"] {
    background: #f3f6fc;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102d4b, #071c32);
}

section[data-testid="stSidebar"] * {
    color: #f4f8ff;
}

section[data-testid="stSidebar"] hr {
    border-color: #39516a;
}

.hero {
    background: linear-gradient(110deg, #dff1ff, #d9f2ff);
    border: 1px solid #d0e8fb;
    border-radius: 18px;
    padding: 26px 30px;
    margin-bottom: 20px;
}

.hero h1 {
    color: #12395e;
    font-size: 2rem;
}

.hero p {
    color: #53728e;
}

.metric-card {
    min-height: 155px;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #e2eaf4;
}

.metric-card h3 {
    font-size: 1rem;
    font-weight: 500;
    color: #24496f;
}

.metric-card .number {
    font-size: 2rem;
    font-weight: 750;
    color: #102f50;
}

.metric-card small {
    color: #64809b;
}

.card-blue { background: #e8f2ff; }
.card-green { background: #e7f7ef; }
.card-purple { background: #f0ebff; }
.card-yellow { background: #fff5dc; }

.section-title {
    color: #14395c;
    font-weight: 750;
    font-size: 1.22rem;
    margin: 20px 0 12px;
}

div.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 600;
}

div.stButton > button[kind="primary"] {
    background: #10151e;
    color: white;
    border-color: #10151e;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e0e9f4;
    padding: 14px;
    border-radius: 14px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #e0e9f4;
    border-radius: 14px;
    background: rgba(255,255,255,.7);
}

.stAlert {
    border-radius: 12px;
}

.github-link {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin: 0 0 12px auto;
}

.github-link a {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border: 1px solid #dbe4ef;
    border-radius: 10px;
    background: white;
    color: #163452 !important;
    text-decoration: none !important;
    font-weight: 600;
}

.github-link a:hover {
    background: #e8f2ff;
}
</style>
""", unsafe_allow_html=True)


# -------------------- GITHUB LINK --------------------

st.markdown("""
<div class="github-link">
    <a href="https://github.com/akshayanandhini546"
       target="_blank" rel="noopener noreferrer">
        <svg width="21" height="21" viewBox="0 0 24 24"
             fill="currentColor" xmlns="http://www.w3.org/2000/svg"
             aria-hidden="true">
            <path d="M12 .8a11.2 11.2 0 0 0-3.54 21.83c.56.1.77-.24.77-.54v-2.1c-3.14.68-3.8-1.33-3.8-1.33-.51-1.3-1.25-1.65-1.25-1.65-1.02-.7.08-.69.08-.69 1.13.08 1.72 1.16 1.72 1.16 1 1.72 2.63 1.22 3.27.93.1-.72.39-1.22.71-1.5-2.5-.29-5.13-1.25-5.13-5.55 0-1.23.44-2.23 1.16-3.02-.12-.29-.5-1.43.11-2.98 0 0 .95-.3 3.08 1.15a10.7 10.7 0 0 1 5.6 0c2.14-1.45 3.08-1.15 3.08-1.15.62 1.55.23 2.69.12 2.98.72.79 1.15 1.79 1.15 3.02 0 4.31-2.63 5.25-5.14 5.53.4.35.75 1.03.75 2.08v3.12c0 .3.2.65.78.54A11.2 11.2 0 0 0 12 .8z"/>
        </svg>
        GitHub ↗
    </a>
</div>
""", unsafe_allow_html=True)


# -------------------- BACKEND FUNCTIONS --------------------

def api_get(path):
    try:
        response = requests.get(f"{API_URL}{path}", timeout=3)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def api_post(path, payload, show_error=True):
    try:
        response = requests.post(
            f"{API_URL}{path}",
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        if show_error:
            st.error(
                "Backend is not responding. Start it using "
                "`py -m backend.server` in another terminal. "
                f"Details: {exc}"
            )
        return None


# -------------------- SIDEBAR --------------------

st.sidebar.markdown("# 🧭 Career Compass")
st.sidebar.caption("Discover your path. Build your future.")
st.sidebar.divider()

pages = {
    "🏠 Home": "Home",
    "👤 Profile": "Profile",
    "🎯 Recommendations": "Recommendations",
    "🗺️ Learning Roadmap": "Learning Roadmap",
    "📊 Skill Gap Analysis": "Skill Gap Analysis",
    "💼 Job Opportunities": "Job Opportunities",
    "💬 Chat Assistant": "Chat Assistant"
}

page = st.sidebar.radio(
    "Navigation",
    list(pages.keys()),
    label_visibility="collapsed"
)
page = pages[page]

st.sidebar.divider()
st.sidebar.info(
    "Create your student profile to get personalized results."
)
st.sidebar.divider()
st.sidebar.caption("Career Compass")
st.sidebar.caption("Your journey to a brighter future ✨")


# -------------------- SESSION DATA --------------------

if "profile" not in st.session_state:
    st.session_state.profile = {
        "student_id": "demo-student",
        "name": "",
        "education": "B.Tech Information Technology",
        "skills": [],
        "interests": [],
        "experience": "Beginner",
        "goal": "Get an internship"
    }

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "roadmap_result" not in st.session_state:
    st.session_state.roadmap_result = None

profile = st.session_state.profile
recs = st.session_state.recommendations


def ensure_recommendations():
    result = api_post("/recommend", profile, show_error=False)
    if result:
        st.session_state.recommendations = result.get(
            "recommendations", []
        )
    return st.session_state.recommendations


def metric_card(icon, title, number, foot, cls):
    st.markdown(f"""
    <div class="metric-card {cls}">
        <div style="font-size:1.35rem">{icon}</div>
        <h3>{title}</h3>
        <div class="number">{number}</div>
        <small>{foot}</small>
    </div>
    """, unsafe_allow_html=True)


# -------------------- HOME --------------------

if page == "Home":

    name = profile.get("name", "").strip() or "Student"

    st.markdown(f"""
    <div class="hero">
        <h1>👋 Hello, {name}!</h1>
        <p>Explore career paths, improve your skills, and plan
        your professional future.</p>
    </div>
    """, unsafe_allow_html=True)

    n_careers = len(recs)
    n_jobs = 8 if recs else 0
    n_learning = 8
    n_gaps = (
        len(recs[0].get("missing_skills", []))
        if recs else 0
    )

    cols = st.columns(4, gap="medium")

    cards = [
        ("💼", "Recommended Career Paths", n_careers,
         "Career matches from your profile", "card-blue"),
        ("👤", "Recommended Job Roles", n_jobs,
         "Career paths to explore", "card-green"),
        ("📚", "Learning Activities", n_learning,
         "Planned learning activities", "card-purple"),
        ("🎯", "Skills to Improve", n_gaps,
         "For your top career match", "card-yellow")
    ]

    for col, args in zip(cols, cards):
        with col:
            metric_card(*args)

    actions = st.columns(4, gap="small")

    labels = [
        ("Explore Careers →", "Recommendations"),
        ("Explore Opportunities →", "Job Opportunities"),
        ("View Learning Plan →", "Learning Roadmap"),
        ("Improve Skills →", "Skill Gap Analysis")
    ]

    for col, (label, destination) in zip(actions, labels):
        with col:
            if st.button(
                label,
                use_container_width=True,
                key=f"home_{destination}"
            ):
                st.info(
                    f"Choose {destination} from the sidebar."
                )

    left, right = st.columns([1.15, 1], gap="large")

    with left:
        st.markdown(
            '<div class="section-title">'
            '⭐ Career Recommendations</div>',
            unsafe_allow_html=True
        )

        if not recs:
            st.info(
                "Save your student profile to generate "
                "personalized recommendations."
            )

            if st.button(
                "Generate My Recommendations",
                type="primary",
                key="home_generate"
            ):
                results = api_post("/recommend", profile)
                if results:
                    st.session_state.recommendations = (
                        results.get("recommendations", [])
                    )
                    st.rerun()
        else:
            for r in recs[:3]:
                with st.container(border=True):
                    st.markdown(f"**{r['title']}**")
                    st.progress(
                        min(max(float(r["match_score"]) / 100, 0), 1)
                    )
                    st.caption(f"Match score: {r['match_score']}%")
                    st.write(r["description"])
                    missing = r.get("missing_skills", [])
                    st.caption(
                        "Skills to improve: "
                        + (", ".join(missing[:4])
                           or "Portfolio and interview practice")
                    )

    with right:
        st.markdown(
            '<div class="section-title">'
            '📘 Your Learning Roadmap</div>',
            unsafe_allow_html=True
        )

        roadmap = st.session_state.roadmap_result

        if roadmap and roadmap.get("steps"):
            for step in roadmap["steps"][:4]:
                st.markdown(
                    f"**🔹 {step['week']}: {step['topic']}**"
                )
                st.caption(step["action"])
        else:
            st.markdown("""
            **Phase 1: Build Strong Fundamentals**

            *Weeks 1–4*

            Python programming · Data structures and problem solving

            **Phase 2: Learn Career Skills**

            *Weeks 5–8*

            Focus on technologies required for your target role.

            **Phase 3: Gain Practical Experience**

            *Weeks 9–10*

            Build a project and publish it on GitHub.

            **Phase 4: Get Career Ready**

            *Weeks 11–12*

            Resume, portfolio and interview practice.
            """)
            st.caption(
                "Generate a personalized roadmap from the "
                "Learning Roadmap page."
            )


# -------------------- PROFILE --------------------

elif page == "Profile":

    st.title("👤 Student Profile")
    st.write(
        "Complete your profile to get career suggestions "
        "based on your current skills and goals."
    )

    with st.form("profile_form"):

        name = st.text_input(
            "Full name", value=profile.get("name", "")
        )

        education_options = [
            "Class XII", "Diploma",
            "B.Tech Information Technology",
            "B.Tech Computer Science", "BCA",
            "B.Sc Computer Science", "Other"
        ]

        education = st.selectbox(
            "Education",
            education_options,
            index=(
                education_options.index(profile["education"])
                if profile.get("education") in education_options
                else 2
            )
        )

        skill_options = [
            "Python", "Java", "C", "SQL", "HTML", "CSS",
            "JavaScript", "React", "Node.js", "Flask",
            "Machine Learning", "Data Analysis", "Excel",
            "Communication", "Git", "MongoDB", "Statistics",
            "Cybersecurity", "Linux", "Cloud Computing",
            "Networking", "Testing", "Database Design",
            "Problem Solving"
        ]

        skills = st.multiselect(
            "Skills you already have",
            skill_options,
            default=[
                s for s in profile.get("skills", [])
                if s in skill_options
            ]
        )

        interest_options = [
            "Web Development", "AI / Machine Learning",
            "Data Science", "Cybersecurity", "Cloud Computing",
            "Software Engineering", "Mobile App Development",
            "Business Analytics", "UI/UX Design",
            "Problem Solving"
        ]

        interests = st.multiselect(
            "Areas of interest",
            interest_options,
            default=[
                s for s in profile.get("interests", [])
                if s in interest_options
            ]
        )

        experience_options = [
            "Beginner", "Student projects",
            "Internship experience", "Experienced"
        ]

        experience = st.selectbox(
            "Experience level",
            experience_options,
            index=(
                experience_options.index(profile["experience"])
                if profile.get("experience") in experience_options
                else 0
            )
        )

        goal_options = [
            "Get an internship", "Get a full-time job",
            "Choose a career path", "Improve my skills",
            "Prepare for placements"
        ]

        goal = st.selectbox(
            "Primary career goal",
            goal_options,
            index=(
                goal_options.index(profile["goal"])
                if profile.get("goal") in goal_options
                else 0
            )
        )

        submit = st.form_submit_button(
            "Save Profile",
            type="primary",
            use_container_width=True
        )

    if submit:
        updated = {
            "student_id": profile.get("student_id", "demo-student"),
            "name": name,
            "education": education,
            "skills": skills,
            "interests": interests,
            "experience": experience,
            "goal": goal
        }

        saved = api_post("/profile", updated)

        if saved:
            st.session_state.profile = updated
            st.success("Your profile has been saved!")
            st.rerun()


# -------------------- RECOMMENDATIONS --------------------

elif page == "Recommendations":

    st.title("🎯 Personalized Career Recommendations")
    st.write(
        "Career matches are ranked using machine-learning "
        "text similarity."
    )

    if st.button("Generate Recommendations", type="primary"):
        result = api_post("/recommend", profile)
        if result:
            st.session_state.recommendations = (
                result.get("recommendations", [])
            )
            st.rerun()

    recs = st.session_state.recommendations

    if not recs:
        st.info(
            "Create your profile and generate recommendations "
            "to see your best-fit career paths."
        )
    else:
        df = pd.DataFrame([
            {
                "Career": r["title"],
                "Match score": r["match_score"]
            }
            for r in recs
        ])

        st.plotly_chart(
            px.bar(
                df,
                x="Match score",
                y="Career",
                orientation="h",
                range_x=[0, 100],
                color="Match score",
                color_continuous_scale=["#dceeff", "#2b79bd"],
                title="Career match scores"
            ),
            use_container_width=True
        )

        for r in recs:
            with st.container(border=True):
                a, b = st.columns([4, 1])

                with a:
                    st.subheader(r["title"])
                    st.write(r["description"])
                    st.caption(
                        "Skills: "
                        + ", ".join(r["required_skills"])
                    )
                    st.write(
                        "**Skills to improve:** "
                        + (", ".join(r["missing_skills"])
                           or "Portfolio and interview practice")
                    )
                    st.write(
                        "**Project ideas:** "
                        + ", ".join(r["projects"])
                    )

                with b:
                    st.metric("Match", f'{r["match_score"]}%')

                    if st.button(
                        "Create roadmap",
                        key=f"create_{r['career_id']}"
                    ):
                        result = api_post(
                            "/roadmap",
                            {
                                "career": r["title"],
                                "skills": profile.get("skills", [])
                            }
                        )
                        if result:
                            st.session_state.roadmap_result = result
                            st.session_state.selected_career = r["title"]
                            st.success(
                                "Roadmap created. Open Learning Roadmap."
                            )


# -------------------- LEARNING ROADMAP --------------------

elif page == "Learning Roadmap":

    st.title("🗺️ Your Learning Roadmap")

    recs = st.session_state.recommendations

    options = [r["title"] for r in recs] or [
        "Software Developer", "Web Developer",
        "Data Analyst", "Machine Learning Engineer"
    ]

    default = st.session_state.get("selected_career", options[0])

    career = st.selectbox(
        "Choose your target career",
        options,
        index=options.index(default) if default in options else 0
    )

    if st.button("Generate Learning Plan", type="primary"):
        result = api_post(
            "/roadmap",
            {
                "career": career,
                "skills": profile.get("skills", [])
            }
        )
        if result:
            st.session_state.roadmap_result = result

    roadmap = st.session_state.roadmap_result

    if roadmap and roadmap.get("steps"):
        for step in roadmap["steps"]:
            with st.container(border=True):
                st.markdown(
                    f"### {step['week']} · {step['topic']}"
                )
                st.write(step["action"])
                st.caption("Deliverable: " + step["deliverable"])
    else:
        st.info(
            "Choose a career and generate a learning plan "
            "to see your personalized weekly roadmap."
        )


# -------------------- SKILL GAP ANALYSIS --------------------

elif page == "Skill Gap Analysis":

    st.title("📊 Skill Gap Analysis")

    if not st.session_state.recommendations:
        ensure_recommendations()

    recs = st.session_state.recommendations

    if not recs:
        st.info(
            "Generate career recommendations first to compare "
            "your skills with target roles."
        )
    else:
        selected = st.selectbox(
            "Target career", [r["title"] for r in recs]
        )

        target = next(
            r for r in recs if r["title"] == selected
        )

        st.metric("Profile match", f'{target["match_score"]}%')

        have, missing = st.columns(2)

        with have:
            st.subheader("✅ Skills you have")
            for skill in target["matched_skills"] or [
                "Add relevant skills to your profile"
            ]:
                st.success(skill)

        with missing:
            st.subheader("🎯 Skills to improve")
            for skill in target["missing_skills"] or [
                "Build projects and practice interviews"
            ]:
                st.warning(skill)

        st.caption(
            "This prototype compares skill names exactly; "
            "equivalent skills may need to be entered manually."
        )


# -------------------- JOB OPPORTUNITIES --------------------

elif page == "Job Opportunities":

    st.title("💼 Job Opportunities")

    st.caption(
        "Sample role ideas only, not live vacancies. "
        "Confirm actual openings on official employer websites."
    )

    path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "opportunities.csv"
    )

    opportunities = pd.read_csv(path).fillna("")

    area = st.selectbox(
        "Career area",
        ["All"] + sorted(
            opportunities["career_area"].unique().tolist()
        )
    )

    if area != "All":
        opportunities = opportunities[
            opportunities["career_area"] == area
        ]

    for _, row in opportunities.iterrows():
        with st.container(border=True):
            st.subheader(row["role"])
            st.caption(
                f"{row['career_area']} · {row['type']} · {row['level']}"
            )
            st.write(row["description"])
            st.write("**Preparation:** " + row["preparation"])
            st.caption(
                "Demo entry — verify current opportunities with employers."
            )


# -------------------- CHAT ASSISTANT --------------------

elif page == "Chat Assistant":

    st.title("💬 Career Guidance Assistant")

    st.caption(
        "This version uses a local rule-based assistant. "
        "A live LLM can be connected as a later enhancement."
    )

    for item in st.session_state.chat_history:
        with st.chat_message(item["role"]):
            st.write(item["content"])

    prompt = st.chat_input(
        "Ask about career paths, skills, internships or interviews..."
    )

    if prompt:
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        result = api_post(
            "/chat",
            {"message": prompt, "profile": profile}
        )

        answer = (
            result.get("answer", "I couldn't generate an answer.")
            if result
            else "Backend unavailable. Start the Flask server and try again."
        )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()
