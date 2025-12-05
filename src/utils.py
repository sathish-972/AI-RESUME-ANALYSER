# src/utils.py
from typing import List, Dict

def badge_for_score(score: int) -> str:
    if score >= 85:
        return "Outstanding"
    if score >= 70:
        return "Strong"
    if score >= 50:
        return "Moderate"
    return "Needs Improvement"


def generate_feedback(skills: List[str], score: int, details: Dict) -> str:
    """
    Generate human-readable feedback using skills, score, and details.
    """
    lines = []
    badge = badge_for_score(score)
    lines.append(f"Overall rating: **{badge}** ({score}%).")

    if not skills:
        lines.append("I couldn’t detect many skills. Make sure you have a clear **Skills** section with bullet points.")
    else:
        lines.append(f"Detected skills: {', '.join(skills)}.")

    word_count = details.get("word_count", 0)
    if word_count < 100:
        lines.append("Your resume seems quite short. Consider adding more details about projects, internships, or responsibilities.")
    elif word_count > 400:
        lines.append("Your resume is fairly long. Try to keep it concise (1 page for students / freshers).")

    # Category-level feedback
    cat_counts = details.get("category_counts", {})
    if cat_counts.get("Technical", 0) == 0:
        lines.append("I don’t see many technical skills. If you are applying for tech roles, highlight programming languages and tools.")
    if cat_counts.get("Soft", 0) == 0:
        lines.append("Try to mention soft skills like teamwork, communication, or problem solving if relevant.")

    jd_match_score = details.get("jd_match_score", 0)
    if jd_match_score > 0:
        lines.append(f"Job match score (based on skills) is around **{jd_match_score}%**.")
        matched = details.get("jd_matched_skills", [])
        if matched:
            lines.append(f"Skills matching the job description: {', '.join(matched)}.")
    else:
        lines.append("For better targeting, paste a job description so I can compare your resume against it.")

    # General tips
    lines.append("\n**Suggestions:**")
    lines.append("- Use bullet points and start them with action verbs (Built, Designed, Implemented, Led...).")
    lines.append("- Quantify achievements where possible (\"Improved X by 20%\", \"Handled Y users\", etc.).")
    lines.append("- Ensure there are no spelling or grammar mistakes.")
    lines.append("- Keep section titles consistent: Summary, Education, Projects, Skills, Achievements.")

    return "\n".join(lines)
