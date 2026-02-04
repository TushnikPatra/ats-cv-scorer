from pdfminer.high_level import extract_text
import docx
import os


def extract_text_from_pdf(file_path: str) -> str:
    try:
        return extract_text(file_path)
    except Exception as e:
        raise RuntimeError(f"PDF extraction failed: {e}")


def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise RuntimeError(f"DOCX extraction failed: {e}")


def extract_resume_text(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError("Resume file not found")

    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")

    return text.strip()
