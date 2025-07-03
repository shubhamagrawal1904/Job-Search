# Resume parser stub
import os
from dotenv import load_dotenv
import pdfplumber
import docx
from llm.llm_setup import get_llm
import json
import re

load_dotenv()

# Helper to extract text from PDF
def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

# Helper to extract text from DOCX
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Main parser function
def parse_resume(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")

    llm = get_llm()
    prompt = f"""
You are a resume parser for job applications. Extract the following fields from the resume text below and return as a JSON object:
- Name
- Email
- Phone
- Location
- Profession
- Education (degree, institution, year)
- Work Experience (company, title, duration, description)
- Skills
- Certifications
- Projects
- LinkedIn URL
- Other relevant info for job applications

Return the result as a JSON object only, with no extra text.

Resume Text:
{text}
"""
    response = llm.invoke(prompt)
    # Extract text from response if it's an object
    if hasattr(response, "content"):
        response_text = response.content
    else:
        response_text = str(response)

    # Extract JSON from the response
    try:
        # Find the first {...} block in the response
        match = re.search(r'\{[\s\S]*\}', response_text)
        if match:
            json_str = match.group(0)
            result = json.loads(json_str)
        else:
            result = {"raw_response": response_text}
    except Exception as e:
        result = {"error": str(e), "raw_response": response_text}
    return result