# src/resume_builder.py

def build_resume_template(sections, skills, style="Modern"):
    """
    Build a resume template using detected sections + skills.
    Supports multiple styles: Modern, Minimal, ATS-friendly.
    """
    summary = sections.get("Summary", "")
    projects = sections.get("Projects", "")
    education = sections.get("Education", "")
    achievements = sections.get("Achievements", "")
    skills_list = ", ".join(skills) if skills else "Add your main skills here"

    if style == "Minimal":
        return f"""
FULL NAME
Email | Phone | City

SUMMARY
{summary or "Write a short 2–3 line summary here."}

SKILLS
{skills_list}

PROJECTS
{projects or "List 2–3 key projects with one line each."}

EDUCATION
{education or "Add your degree, college, and year of passing."}

ACHIEVEMENTS
{achievements or "Mention certifications, awards, or hackathons here."}
""".strip()

    if style == "ATS-friendly":
        return f"""
FULL NAME
Email: your.email@example.com
Phone: +91 XXXXX XXXXX
LinkedIn: https://linkedin.com/in/yourprofile

SUMMARY:
{summary or "Results-driven student/professional with skills in <your domain>."}

SKILLS:
{skills_list}

EXPERIENCE:
- Add job/internship title | Company | Dates
  - Use bullet points with action verbs and measurable impact.

PROJECTS:
{projects or "- Add 2–4 projects, each with tech stack and what you built."}

EDUCATION:
{education or "- Degree | College | Year | CGPA"}

ACHIEVEMENTS:
{achievements or "- Add certifications, awards, competitive exams, etc."}

DECLARATION:
I hereby declare that the information furnished above is true to the best of my knowledge.
""".strip()

    # Default: Modern
    return f"""
=============================================
               MODERN RESUME
=============================================

FULL NAME
Email: your.email@example.com
Phone: +91 XXXXX XXXXX
LinkedIn: linkedin.com/in/yourprofile
GitHub: github.com/yourgithub

---------------------------------------------
SUMMARY
---------------------------------------------
{summary or "Write a 3–4 line summary describing your strengths, skills, and goals."}

---------------------------------------------
SKILLS
---------------------------------------------
{skills_list}

---------------------------------------------
PROJECTS
---------------------------------------------
{projects or "Add your top 2–4 projects here with impact & responsibilities."}

---------------------------------------------
EDUCATION
---------------------------------------------
{education or "Add your school/college details here."}

---------------------------------------------
ACHIEVEMENTS
---------------------------------------------
{achievements or "Add certificates, awards, hackathons, etc."}

---------------------------------------------
EXPERIENCE (OPTIONAL)
---------------------------------------------
Add your internships or work experience here.

---------------------------------------------
DECLARATION
---------------------------------------------
I hereby declare that all the information provided above is true to the best of my knowledge.

=============================================
""".strip()
