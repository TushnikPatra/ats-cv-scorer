from utils import clean_text


def keyword_match_score(resume_text: str, jd_keywords: list) -> dict:
    resume_text = clean_text(resume_text)

    matched = []
    missing = []

    for keyword in jd_keywords:
        if keyword in resume_text:
            matched.append(keyword)
        else:
            missing.append(keyword)

    if not jd_keywords:
        score = 0
    else:
        score = (len(matched) / len(jd_keywords)) * 100

    return {
        "score": round(score, 2),
        "matched_keywords": matched,
        "missing_keywords": missing
    }
def section_presence_score(resume_text: str) -> dict:
    resume_text = resume_text.lower()

    sections = {
        "experience": ["experience", "work experience", "employment"],
        "skills": ["skills", "technical skills"],
        "education": ["education", "academic"],
        "projects": ["projects", "certifications"]
    }

    found_sections = []
    missing_sections = []

    for section, keywords in sections.items():
        if any(keyword in resume_text for keyword in keywords):
            found_sections.append(section)
        else:
            missing_sections.append(section)

    score = (len(found_sections) / len(sections)) * 100

    return {
        "score": round(score, 2),
        "found_sections": found_sections,
        "missing_sections": missing_sections
    }
def formatting_score(resume_text: str) -> dict:
    penalties = 0
    issues = []

    # Very basic ATS red flags
    if "|" in resume_text:
        penalties += 20
        issues.append("Excessive use of separators (|)")

    if "\t" in resume_text:
        penalties += 20
        issues.append("Tab-based layout detected")

    if resume_text.count("\n") < 20:
        penalties += 30
        issues.append("Low text content (possible image-based resume)")

    score = max(0, 100 - penalties)

    return {
        "score": score,
        "issues": issues
    }

def final_ats_score(keyword_result: dict,
                    section_result: dict,
                    formatting_result: dict) -> float:

    final_score = (
        keyword_result["score"] * 0.6 +
        section_result["score"] * 0.3 +
        formatting_result["score"] * 0.1
    )

    return round(final_score, 2)
