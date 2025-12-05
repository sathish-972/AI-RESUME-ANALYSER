import io
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from pdfminer.high_level import extract_text


# 🪟 Optional: specify tesseract path (only if OCR fails)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from any kind of resume (text, scanned, or hybrid PDFs).
    Combines PyMuPDF, pdfminer, and OCR for maximum reliability.
    Returns full cleaned text.
    """
    text = ""
    ocr_used = False  # flag for debugging or reporting

    try:
        uploaded_file.seek(0)
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page_count = pdf_doc.page_count

        for i, page in enumerate(pdf_doc):
            # ✅ Try normal text extraction
            page_text = page.get_text("text")

            # 🧠 Fallback: OCR if page has little or no text
            if len(page_text.strip()) < 100:
                ocr_used = True
                pix = page.get_pixmap(dpi=300)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                page_text = pytesseract.image_to_string(img)

            text += page_text + "\n\n"

        pdf_doc.close()

    except Exception as e:
        print("PyMuPDF extraction failed:", e)

    # ✅ If PyMuPDF didn’t capture enough, try pdfminer
    if len(text.strip()) < 500:
        try:
            uploaded_file.seek(0)
            text = extract_text(uploaded_file)
        except Exception as e:
            print("pdfminer fallback failed:", e)

    clean = clean_text(text)
    return clean.strip(), ocr_used, page_count


def clean_text(text: str) -> str:
    """Smart cleaning: removes symbols, fixes spacing and broken words."""
    # Remove unreadable artifacts or junk chars
    text = re.sub(r"[^A-Za-z0-9.,;:@/\-\n\s()&%+*]+", " ", text)

    # Normalize whitespace
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s{2,}", " ", text)

    # Common cleanup replacements
    replacements = {
        " ,": ",",
        " .": ".",
        " - ": "-",
        "–": "-",
        "—": "-",
        "…": "",
        "•": "",
        "§": "",
        "ï": "",
        "’": "'",
        "ﬁ": "fi",
        "ﬂ": "fl",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Fix truncated "Univers..." etc.
    text = re.sub(r"\bUnivers\.*\b", "University", text, flags=re.IGNORECASE)

    return text.strip()
