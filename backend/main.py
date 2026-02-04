from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware

from parser import extract_resume_text
from utils import extract_keywords
from scorer import (
    keyword_match_score,
    section_presence_score,
    formatting_score,
    final_ats_score
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ats-score")
async def ats_score(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    temp_file = f"temp_{resume.filename}"

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    resume_text = extract_resume_text(temp_file)
    os.remove(temp_file)

    jd_keywords = extract_keywords(job_description)

    keyword_result = keyword_match_score(resume_text, jd_keywords)
    section_result = section_presence_score(resume_text)
    formatting_result = formatting_score(resume_text)

    final_score = final_ats_score(
        keyword_result,
        section_result,
        formatting_result
    )

    return {
        "final_ats_score": final_score,
        "keyword_score": keyword_result["score"],
        "matched_keywords": keyword_result["matched_keywords"],
        "missing_keywords": keyword_result["missing_keywords"],
        "section_score": section_result["score"],
        "missing_sections": section_result["missing_sections"],
        "formatting_score": formatting_result["score"],
        "formatting_issues": formatting_result["issues"]
    }


