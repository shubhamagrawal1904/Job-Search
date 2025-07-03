# Job Application AI Agent

## Overview
This project is an AI-powered agent that automates job applications using your resume. It parses your resume, searches for relevant jobs on LinkedIn and Naukri, generates tailored cover letters, applies for jobs, and tracks applications in Excel. If information is missing from your resume, it will ask you for input.

## Features
- Resume parsing (PDF/DOCX)
- Job search (LinkedIn, Naukri)
- Automated job application
- Cover letter generation
- Human-in-the-loop for missing info
- Application tracking in Excel
- Modular, production-grade codebase
- Workflow managed by LangGraph

## Setup
1. Install [uv](https://github.com/astral-sh/uv):
   ```sh
   pip install uv
   ```
2. Install dependencies:
   ```sh
   uv pip install -r requirements.txt
   ```
3. Run the agent:
   ```sh
   python main.py
   ```

## Folder Structure
- `agents/`: Agent and workflow logic
- `components/`: Modular components (parsing, search, etc.)
- `utils/`: Utilities (Excel, logging)
- `data/`: Stores applied jobs Excel 