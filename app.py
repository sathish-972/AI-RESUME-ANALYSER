import streamlit as st
import sys
import os
import matplotlib.pyplot as plt

# Make sure we can import from src/
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from extractor import extract_text_from_pdf
from nlp import analyze_resume_text
from utils import generate_feedback
from sections import detect_sections
from resume_builder import build_resume_template


# ---------- Helper: ATS Breakdown ---------- #
def compute_ats_breakdown(details, sections):
    """
    Compute simple ATS-style component scores.
    Components: Skills, Keywords, Structure, Length.
    """
    word_count = details.get("word_count", 0)
    num_skills = details.get("num_skills", 0)
    jd_match = details.get("jd_match_score", 0)

    # Skills: up to 40 points
    skills_score = min(num_skills * 5, 40)

    # Keywords (JD match): up to 30 points
    keyword_score = min(jd_match, 30)

    # Structure: based on number of sections detected: up to 20 points
    num_sections = len([s for s in sections.values() if s.strip()])
    structure_score = min(num_sections * 4, 20)

    # Length: 0–10 based on ideal word range
    if 120 <= word_count <= 450:
        length_score = 10
    elif 80 <= word_count < 120 or 450 < word_count <= 600:
        length_score = 6
    else:
        length_score = 2

    total = min(skills_score + keyword_score + structure_score + length_score, 100)

    return int(total), {
        "Skills": int(skills_score),
        "Keywords": int(keyword_score),
        "Structure": int(structure_score),
        "Length": int(length_score),
    }


def build_quick_suggestions(word_count, num_skills, jd_match, ats_score, sections_count):
    suggestions = []

    # Length
    if word_count < 120:
        suggestions.append("Add more content: projects, internships, or responsibilities.")
    elif word_count > 450:
        suggestions.append("Try to reduce length: keep it concise (1–2 pages).")

    # Skills
    if num_skills < 5:
        suggestions.append("Add more relevant skills in a dedicated Skills section.")
    elif num_skills > 15:
        suggestions.append("Group similar skills and avoid listing too many buzzwords.")

    # Job match
    if jd_match > 0 and jd_match < 60:
        suggestions.append("Tailor your skills and keywords to better match the job description.")
    elif jd_match >= 60:
        suggestions.append("Good job match — highlight your strongest matching skills on top.")

    # Sections
    if sections_count < 4:
        suggestions.append("Consider adding standard sections: Summary, Skills, Projects, Education, Achievements.")

    # ATS
    if ats_score < 60:
        suggestions.append("Focus on improving skills, structure, and keywords to boost ATS score.")
    else:
        suggestions.append("ATS score is decent — refine wording and quantify achievements.")

    if not suggestions:
        suggestions.append("Your resume looks well-structured. Fine-tune wording and formatting for extra polish.")

    return suggestions


# ---------- Page config + Dark Professional UI ---------- #

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide",
    page_icon="📄",
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #020617;
            font-family: "Segoe UI", system-ui, sans-serif;
            color: #e5e7eb;
        }
        .top-bar {
            background: linear-gradient(90deg, #1d4ed8, #4f46e5);
            padding: 14px 24px;
            border-radius: 0 0 12px 12px;
            color: #f9fafb;
            margin-bottom: 18px;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.6);
        }
        .app-title {
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 2px;
        }
        .app-subtitle {
            font-size: 13px;
            opacity: 0.9;
        }
        .card {
            background-color: #020617;
            border-radius: 10px;
            padding: 16px 18px;
            border: 1px solid #1f2937;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.9);
            margin-bottom: 18px;
        }
        .section-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #e5e7eb;
        }
        textarea, .stTextArea textarea {
            color: #e5e7eb !important;
            background-color: #020617 !important;
        }
        .stDownloadButton > button, .stButton > button {
            border-radius: 999px;
            padding: 0.4rem 1.1rem;
            border: 1px solid #374151;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Top header bar
st.markdown(
    """
    <div class="top-bar">
        <div class="app-title">📄 AI Resume Analyzer</div>
        <div class="app-subtitle">
            Analyze your resume, simulate ATS scoring, get instant suggestions, and generate professional templates.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Session State ---------- #

if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "last_file" not in st.session_state:
    st.session_state.last_file = None

# ---------- Inputs ---------- #

col_input1, col_input2 = st.columns([1.1, 1.9])

with col_input1:
    uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

with col_input2:
    job_description = st.text_area(
        "Optional: Paste Job Description for match analysis",
        height=120,
        placeholder="Paste the target job description here...",
    )

# Reset analysis when a new file is uploaded
if uploaded_file is not None:
    if st.session_state.last_file != uploaded_file.name:
        st.session_state.analysis = None
        st.session_state.last_file = uploaded_file.name

# ---------- Main logic ---------- #

if uploaded_file is not None:
    # Extract text
    with st.spinner("Extracting text from resume..."):
        try:
            resume_text, ocr_used, pages = extract_text_from_pdf(uploaded_file)
        except Exception as e:
            st.error(f"Error extracting text: {e}")
            st.stop()

    # Top row: extraction + length
    top1, top2 = st.columns(2)

    with top1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Extraction Summary</div>', unsafe_allow_html=True)
        st.write(f"📄 Pages detected: **{pages}**")
        if ocr_used:
            st.warning("OCR was used (scanned/image-based PDF detected).")
        else:
            st.success("Extracted text directly (text-based PDF).")
        st.markdown('</div>', unsafe_allow_html=True)

    with top2:
        word_count = len(resume_text.split())
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Resume Length Check</div>', unsafe_allow_html=True)
        st.write(f"Total words: **{word_count}**")
        if word_count < 120:
            st.warning("Resume is **too short**. Add more details, projects, or experience.")
        elif word_count > 450:
            st.error("Resume is **too long**. Try to keep it concise (1–2 pages).")
        else:
            st.success("Resume length is in a good range.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Middle row: text preview + sections
    mid1, mid2 = st.columns([2, 1])

    with mid1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Extracted Resume Text (Preview)</div>', unsafe_allow_html=True)
        preview = resume_text[:2500] + "..." if len(resume_text) > 2500 else resume_text
        st.text_area("Extracted Text", preview, height=320)
        st.markdown('</div>', unsafe_allow_html=True)

    with mid2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Detected Resume Sections</div>', unsafe_allow_html=True)
        sections = detect_sections(resume_text)
        if sections:
            for sec_name, sec_content in sections.items():
                with st.expander(f"📂 {sec_name}"):
                    st.write(sec_content)
        else:
            st.info("No major sections automatically detected.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Analyze button
    if st.button("🔍 Analyze Resume"):
        with st.spinner("Running analysis..."):
            try:
                skills, score, details = analyze_resume_text(resume_text, job_description)
                feedback = generate_feedback(skills, score, details)
                ats_score, ats_components = compute_ats_breakdown(details, sections)
            except Exception as e:
                st.error(f"Error analyzing resume: {e}")
                st.stop()

        st.session_state.analysis = {
            "skills": skills,
            "score": score,
            "details": details,
            "feedback": feedback,
            "sections": sections,
            "resume_text": resume_text,
            "ats_score": ats_score,
            "ats_components": ats_components,
        }
        st.success("Analysis complete. Scroll down to view results.")

    # Show results if we have them
    analysis = st.session_state.analysis
    if analysis is not None:
        skills = analysis["skills"]
        score = analysis["score"]
        details = analysis["details"]
        feedback = analysis["feedback"]
        sections = analysis["sections"]
        resume_text = analysis["resume_text"]
        ats_score = analysis["ats_score"]
        ats_components = analysis["ats_components"]
        jd_match = details.get("jd_match_score", 0)
        sections_count = len([s for s in sections.values() if s.strip()])

        tab_overview, tab_ats, tab_dash = st.tabs(["Overview", "ATS Breakdown", "Dashboard"])

        # ----- OVERVIEW ----- #
        with tab_overview:
            o1, o2 = st.columns([1.7, 1.3])

            with o1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Detected Skills</div>', unsafe_allow_html=True)
                if skills:
                    st.write(", ".join(skills))
                else:
                    st.write("No skills detected. Consider adding a dedicated Skills section.")
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">AI Feedback</div>', unsafe_allow_html=True)
                st.markdown(feedback)
                st.markdown('</div>', unsafe_allow_html=True)

            with o2:
                # Scores card
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Scores</div>', unsafe_allow_html=True)
                st.metric("Resume Score", f"{score} / 100")
                if jd_match > 0:
                    st.metric("Job Match Score", f"{jd_match} / 100")
                st.metric("ATS Simulator Score", f"{ats_score} / 100")
                st.markdown('</div>', unsafe_allow_html=True)

                # Suggestion bar card
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">💡 Suggestion Bar</div>', unsafe_allow_html=True)
                suggestions = build_quick_suggestions(
                    details.get("word_count", 0),
                    details.get("num_skills", 0),
                    jd_match,
                    ats_score,
                    sections_count,
                )
                for s in suggestions:
                    st.write(f"- {s}")
                st.markdown('</div>', unsafe_allow_html=True)

            # Resume templates
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Auto-Generated Resume Template</div>', unsafe_allow_html=True)

            template_style = st.radio(
                "Choose template style",
                ["Modern", "Minimal", "ATS-friendly"],
                index=0,
                horizontal=True,
            )

            generated_resume = build_resume_template(sections, skills, style=template_style)

            st.text_area("Generated Resume", generated_resume, height=320)

            st.download_button(
                f"Download {template_style} Resume (.txt)",
                data=generated_resume,
                file_name=f"generated_resume_{template_style.lower().replace(' ', '_')}.txt",
                mime="text/plain",
            )

            st.markdown('</div>', unsafe_allow_html=True)

            # Download extracted text
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Download Extracted Text</div>', unsafe_allow_html=True)
            st.download_button(
                "Download extracted text as .txt",
                data=resume_text,
                file_name="extracted_resume_text.txt",
                mime="text/plain",
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # ----- ATS BREAKDOWN ----- #
        with tab_ats:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">ATS Score Breakdown</div>', unsafe_allow_html=True)

            st.write(
                "Approximate breakdown of how an ATS-like system might score your resume "
                "based on **Skills**, **Keywords**, **Structure**, and **Length**."
            )

            st.metric("Overall ATS Score", f"{ats_score} / 100")

            labels = list(ats_components.keys())
            values = list(ats_components.values())

            fig, ax = plt.subplots()
            ax.bar(labels, values, color=["#3b82f6", "#22c55e", "#f97316", "#a855f7"])
            ax.set_ylim(0, 100)
            ax.set_ylabel("Score (0–100)")
            ax.set_title("ATS Component Scores")
            st.pyplot(fig)

            st.markdown("**What this means:**")
            st.write(
                "- **Skills**: How many relevant skills were detected.\n"
                "- **Keywords**: Overlap of your skills with the job description.\n"
                "- **Structure**: Presence of standard sections (Summary, Skills, Projects, etc.).\n"
                "- **Length**: Whether the resume length is in a typical ATS-friendly range."
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # ----- DASHBOARD ----- #
        with tab_dash:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Resume Insights Dashboard</div>', unsafe_allow_html=True)

            d1, d2 = st.columns(2)

            with d1:
                st.markdown("**Skill Categories**")
                cat_counts = details.get("category_counts", {})
                if cat_counts:
                    fig2, ax2 = plt.subplots()
                    ax2.bar(cat_counts.keys(), cat_counts.values(), color="#0ea5e9")
                    ax2.set_ylabel("Count")
                    ax2.set_title("Detected Skill Categories")
                    st.pyplot(fig2)
                else:
                    st.info("No skills available to show category chart.")

            with d2:
                st.markdown("**Key Numbers**")
                st.write(f"- Word count: **{details.get('word_count', 0)}**")
                st.write(f"- Skills detected: **{details.get('num_skills', 0)}**")
                st.write(f"- Job match (skills vs JD): **{jd_match}%**")
                st.write(f"- Sections detected: **{sections_count}**")

            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 Upload a PDF resume to get started.")
