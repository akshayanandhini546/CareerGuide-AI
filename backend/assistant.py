def answer_question(question, profile=None):
    """Simple local fallback. Connect an LLM API here for generative responses."""
    q = (question or "").lower()
    profile = profile or {}
    skills = ", ".join(profile.get("skills", [])) or "your current skills"
    goal = profile.get("goal", "explore career options")

    if any(word in q for word in ["resume", "cv"]):
        return "Keep your resume to one page if you are early in your career. Add education, technical skills, 2–3 projects, internships/certificates, and measurable outcomes. Tailor the skills section to each role."
    if any(word in q for word in ["interview", "placement"]):
        return "Prepare a 60-second introduction, revise core concepts, practice coding/problem-solving, and prepare clear explanations of two projects. Use mock interviews and review each mistake."
    if any(word in q for word in ["skill", "learn", "roadmap"]):
        return f"Your current profile includes: {skills}. For your goal to {goal}, choose one target role, learn its missing fundamentals, build a small project, publish it on GitHub, and then practice interview questions."
    if any(word in q for word in ["internship", "job", "opportunity"]):
        return "Use the opportunities section as a starting point, then verify each opening on the employer's official careers page. Keep your resume and GitHub portfolio ready, and track application deadlines."
    return f"Start with your interests, current skills ({skills}), and goal ({goal}). Compare the top recommended roles, review the missing skills, and follow the learning roadmap. This demo assistant uses predefined guidance rather than a live LLM."
