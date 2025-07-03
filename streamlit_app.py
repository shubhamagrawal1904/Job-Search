import streamlit as st
from components.resume_parser import parse_resume
from components.rss_job_search import get_jobs_with_llm
from components.cover_letter_generator import generate_cover_letter
from utils.json_utils import save_json, load_json
import tempfile
import os
import json
import pandas as pd

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

st.title("AI Resume & Job Search (RSS + LLM)")

config = load_config()

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
rss_url = st.text_input("Enter RSS feed URL for jobs")

resume_info = None
jobs_info = None

if uploaded_file and rss_url:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    st.info("Parsing your resume with Groq LLM...")
    try:
        resume_info = parse_resume(tmp_path)
        st.success("Resume parsed successfully!")
        st.subheader("Extracted Resume Information:")
        st.json(resume_info)
        save_json(resume_info, config['resume_info_path'])
        st.info("Saved resume info JSON.")

        st.info("Fetching and parsing jobs from RSS feed with LLM...")
        jobs_info = get_jobs_with_llm(rss_url, max_jobs=5, delay=2)
        st.success("Job search completed!")
        st.subheader("Job Info Extracted:")
        # Generate cover letter for each job
        for job in jobs_info:
            cover_letter = generate_cover_letter(resume_info, job)
            job['cover_letter'] = cover_letter
        st.json(jobs_info)
        save_json(jobs_info, config['job_info_path'])
        st.info("Saved job info JSON (with cover letters).")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        os.remove(tmp_path)

# Download buttons for resume JSON and jobs Excel
if os.path.exists(config['resume_info_path']):
    with open(config['resume_info_path'], 'rb') as f:
        st.download_button("Download Resume JSON", f, file_name="resume_info.json", mime="application/json")

if os.path.exists(config['job_info_path']):
    jobs_info = load_json(config['job_info_path'])
    # Flatten job info for DataFrame
    def flatten_job(job):
        flat = job.copy()
        if isinstance(flat.get('top_skills_required'), list):
            flat['top_skills_required'] = ', '.join(flat['top_skills_required'])
        flat['cover_letter'] = flat.get('cover_letter', '')
        return flat
    jobs_flat = [flatten_job(j) for j in jobs_info]
    df = pd.DataFrame(jobs_flat)
    excel_path = os.path.join('data', 'jobs_info.xlsx')
    df.to_excel(excel_path, index=False)
    with open(excel_path, 'rb') as f:
        st.download_button("Download Jobs Excel", f, file_name="jobs_info.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.write("Please upload a resume and enter an RSS feed URL to begin.") 