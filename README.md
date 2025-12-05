# AI-RESUME-ANALYSER
📄 AI Resume Analyzer
A powerful AI-driven tool that analyzes resumes, extracts text, evaluates ATS scores, and generates professional resume templates.

🚀 Features
🔍 Resume Text Extraction

Extracts text from normal PDFs and scanned PDFs using OCR

Uses PyMuPDF, Tesseract, and fallback methods for best accuracy

🤖 AI Resume Analysis

Detects important resume sections (Summary, Skills, Projects, Education, Achievements)

Identifies skills & technical keywords

Generates detailed improvement suggestions

Calculates:

Resume Score

Job Match Score (using pasted job description)

ATS Score

📊 ATS Simulation

Breakdown of:

Skill Relevance

Keyword Match

Structure Score

Length Score

Includes charts and visual breakdowns.

📝 Auto Resume Builder

Generates 3 professional templates:

Modern

Minimal

ATS-Friendly

Users can download generated resumes as .txt.

🎛️ Interactive Dashboard

Word count analysis

Skills category chart

Section completeness

Job match insights

🌑 Dark Mode Professional UI

Clean, sleek and modern

Easy to read and navigate

Built with Streamlit custom CSS styling

🏗️ Tech Stack
Frontend / UI

Streamlit (Custom Dark UI)

AI / NLP

NLTK

Custom rule-based section detection

Keyword extraction

ATS scoring algorithm

PDF Processing

PyMuPDF

Tesseract OCR

Pillow

Visualization

Matplotlib

📁 Project Structure
AI-RESUME-ANALYSER/
│  app.py
│  requirements.txt
│  README.md
│
├─ src/
│   ├─ extractor.py
│   ├─ nlp.py
│   ├─ utils.py
│   ├─ sections.py
│   └─ resume_builder.py
│
└─ .gitignore

⚙️ Installation & Running Locally
1️⃣ Clone the repo
git clone https://github.com/sathish-972/AI-RESUME-ANALYSER
cd AI-RESUME-ANALYSER

2️⃣ Create virtual environment
python -m venv .venv

3️⃣ Activate the environment
Windows:
.venv\Scripts\activate

4️⃣ Install dependencies
pip install -r requirements.txt

5️⃣ Run the app
streamlit run app.py

🌐 Deployment (Streamlit Cloud)

Go to https://streamlit.io

Connect your GitHub

Deploy your repo:

Repository: sathish-972/AI-RESUME-ANALYSER

Branch: main

Main file: app.py

The app will auto-deploy and generate a public link!

🧪 Demo Video / Screenshots (Optional)

(You can add screenshots later to make the repo look premium)

🧑‍💻 Author

Sathish
GitHub: sathish-972
