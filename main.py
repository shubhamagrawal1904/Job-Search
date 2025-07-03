from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from components.resume_parser import parse_resume
from components.rss_job_search import get_jobs_with_llm
from components.cover_letter_generator import generate_cover_letter
import tempfile
import os
import json

app = FastAPI()

@app.post("/process_resume_and_jobs/")
async def process_resume_and_jobs(
    resume: UploadFile = File(...),
    rss_url: str = Form(...)
):
    # Save uploaded resume to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume.filename)[-1]) as tmp_file:
        tmp_file.write(await resume.read())
        tmp_path = tmp_file.name
    try:
        resume_info = parse_resume(tmp_path)
        jobs_info = get_jobs_with_llm(rss_url, max_jobs=5, delay=2)
        for job in jobs_info:
            cover_letter = generate_cover_letter(resume_info, job)
            job['cover_letter'] = cover_letter
        return JSONResponse({
            "resume_info": resume_info,
            "jobs_info": jobs_info
        })
    finally:
        os.remove(tmp_path) 