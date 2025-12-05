# src/nlp.py
import re
from collections import Counter
from typing import Tuple, List, Dict, Optional

# Basic skills you can expand anytime
TECH_SKILLS = [
    "python", "java", "c++", "javascript", "react", "node", "html", "css",
    "machine learning", "deep learning", "tensorflow", "pytorch",
    "data science", "sql", "mongodb", "git", "docker", "aws", "azure",
    "flask", "streamlit", "excel", "tableau", "power bi", "pandas", "numpy"
]

SOFT_SKILLS = [
    "leadership", "communication", "teamwork", "problem solving",
    "creativity", "adaptability", "time management", "collaboration",
    "critical thinking", "decision making", "analytical thinking"
]

CATEGORIES = {
    "Technical": TECH_SKILLS,
    "Soft": SOFT_SKILLS,
}


def analyze_resume_text(
    resume_text: str,
    job_description: Optional[str] = None
) -> Tuple[List[str], int, Dict]:
    """
    Analyze resume text:
      - detect skills (technical + soft)
      - compute a resume score (0-100)
      - optionally compute job match score vs job_description

    Returns: (skills_list, score, details_dict)
    """
    text_lower = resume_text.lower()

    found_pairs = []  # list of (skill, category)
    for category, skills in CATEGORIES.items():
        for skill in skills:
            # word-boundary match
            if re.search(r"\b" + re.escape(skill) + r"\b", text_lower):
                found_pairs.append((skill, category))

    # de-duplicate skills while preserving category counts
    seen = set()
    skills_ordered: List[str] = []
    cat_counter = Counter()
    for skill, cat in found_pairs:
        if skill not in seen:
            seen.add(skill)
            skills_ordered.append(skill.capitalize())
            cat_counter[cat] += 1

    num_skills = len(skills_ordered)
    word_count = len(resume_text.split())

    # base score from skill count + length
    base_score = min(100, 20 + num_skills * 4)
    if word_count < 80:
        base_score = max(30, base_score - 10)  # penalize too-short resumes

    # Optional job description matching
    jd_match_score = 0
    jd_matched_skills: List[str] = []
    if job_description:
        jd_text = job_description.lower()
        for skill in skills_ordered:
            if skill.lower() in jd_text:
                jd_matched_skills.append(skill)
        if skills_ordered:
            jd_match_score = int(round(len(jd_matched_skills) / len(skills_ordered) * 100))

        # blend into final score
        base_score = int(round(base_score * 0.7 + jd_match_score * 0.3))

    details = {
        "word_count": word_count,
        "num_skills": num_skills,
        "category_counts": dict(cat_counter),
        "jd_match_score": jd_match_score,
        "jd_matched_skills": jd_matched_skills,
    }

    return skills_ordered, base_score, details
