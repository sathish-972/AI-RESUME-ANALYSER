import re

SECTION_PATTERNS = {
    "Summary": r"(summary|objective)",
    "Skills": r"(skills|technical skills|skill set)",
    "Projects": r"(projects|work experience|experience|internship)",
    "Education": r"(education|academic|qualification)",
    "Achievements": r"(achievements|awards|certifications)",
}

def detect_sections(text: str):
    """
    Detect major sections of a resume using regex.
    Returns a dictionary: {section_name: content}
    """
    clean = text.replace("\n", " ")
    clean = re.sub(r"\s{2,}", " ", clean)

    sections_found = {}
    matches = []

    # find section headers
    for name, pattern in SECTION_PATTERNS.items():
        match = re.search(pattern, clean, re.IGNORECASE)
        if match:
            matches.append((name, match.start()))

    # if no matches
    if not matches:
        return {}

    matches.sort(key=lambda x: x[1])

    # slice text between indexed sections
    for i in range(len(matches)):
        name, start = matches[i]
        end = matches[i + 1][1] if i + 1 < len(matches) else len(clean)
        content = clean[start:end]
        content = re.sub(r"(?i)" + SECTION_PATTERNS[name], "", content).strip()
        sections_found[name] = content

    return sections_found
