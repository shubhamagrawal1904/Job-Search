# Cover letter generator stub
import os
from dotenv import load_dotenv
from llm.llm_setup import get_llm
import re

load_dotenv()

def generate_cover_letter(resume_info, job_info):
    llm = get_llm()
    resume_text = f"Name: {resume_info.get('Name', '')}\n" \
                  f"Email: {resume_info.get('Email', '')}\n" \
                  f"Phone: {resume_info.get('Phone', '')}\n" \
                  f"Location: {resume_info.get('Location', '')}\n" \
                  f"Education: {resume_info.get('Education', '')}\n" \
                  f"Experience: {resume_info.get('Work Experience', '')}\n" \
                  f"Skills: {resume_info.get('Skills', '')}\n"
    job_title = job_info.get('job_title') or job_info.get('title_from_rss') or ''
    company = job_info.get('company', '')
    job_skills = job_info.get('top_skills_required', [])
    job_summary = job_info.get('summary', '')
    job_desc = f"Job Title: {job_title}\nCompany: {company}\nSkills Required: {', '.join(job_skills)}\nJob Description: {job_summary}"
    prompt = f"""
Write a professional cover letter for the following job application. Use the candidate's resume information and align their skills and experience with the job requirements. Highlight why the candidate is a great fit for the role.

Resume Information:
{resume_text}

Job Information:
{job_desc}

Return only the cover letter text. Do not include any tags, commentary, or code blocks.
"""
    response = llm.invoke(prompt)
    text = response.content if hasattr(response, "content") else str(response)
    # Remove code blocks, <think> tags, and extra whitespace
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'<think>[\s\S]*?</think>', '', text, flags=re.IGNORECASE)
    text = text.strip()
    return text 