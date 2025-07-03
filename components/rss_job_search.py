import ssl
import feedparser
import json
import requests
from llm.llm_setup import get_llm
import os
from dotenv import load_dotenv
import time

# Disable SSL certificate verification globally
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LLM-based job info extraction
def extract_job_info_with_llm(html, url):
    llm = get_llm()
    prompt = f"""
You are an expert job information extractor. Given the HTML content of a job posting page, extract the following fields and return them as a JSON object:
- Job Title
- Company
- Location
- HR Details (if any)
- HR Email (if any)
- Date Posted
- Number of Applicants (if any)
- Top Skills Required
- Experience
- Summary of the job

If a field is not present, use null.

Job URL: {url}

HTML Content:
{html[:12000]}
"""
    response = llm.invoke(prompt)
    try:
        response_text = response.content if hasattr(response, "content") else str(response)
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_str = response_text[json_start:json_end]
        return json.loads(json_str)
    except Exception as e:
        return {"error": str(e), "raw_response": response_text}

def get_jobs_with_llm(rss_url, max_jobs=5, delay=2):
    jobs = []
    feed = feedparser.parse(rss_url)
    for entry in feed.entries[:max_jobs]:
        link = entry.link
        try:
            resp = requests.get(link, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if resp.status_code == 200:
                job_info = extract_job_info_with_llm(resp.text, link)
                job_info['title_from_rss'] = entry.title
                job_info['link'] = link
                jobs.append(job_info)
            else:
                jobs.append({"error": f"Failed to fetch {link} (status {resp.status_code})", "link": link})
        except Exception as e:
            jobs.append({"error": str(e), "link": link})
        time.sleep(delay)
    return jobs

# if __name__ == "__main__":
#     # Example RSS feed (replace with a real job RSS feed URL)
#     rss_url = input("Enter RSS feed URL: ")
#     jobs = get_jobs_with_llm(rss_url,max_jobs=2,delay=2)
#     print(json.dumps(jobs, indent=2)) 