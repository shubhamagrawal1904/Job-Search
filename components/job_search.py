# Job search stub
import requests
from bs4 import BeautifulSoup

# Basic Naukri job search using parsed resume info
def search_jobs(parsed_resume):
    # Extract relevant fields
    skills = parsed_resume.get('Profession', '')
    job_title = parsed_resume.get('Work Experience', [{}])[0].get('title', '') if parsed_resume.get('Work Experience') else ''
    location = parsed_resume.get('Location', '')

    # Formulate search query
    query = f"{skills}".strip().replace(' ', '-')
    print(query)
    location_query = location.replace(' ', '-') if location else ''
    url = f"https://www.naukri.com/{query}-jobs-in-{location_query}"
    print(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    jobs = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('article', class_='jobTuple')
        print('Job Cards',job_cards)
        for card in job_cards[:10]:  # Limit to 10 jobs
            title = card.find('a', class_='title')
            company = card.find('a', class_='subTitle')
            location = card.find('li', class_='location')
            link = title['href'] if title else ''
            jobs.append({
                'title': title.text.strip() if title else '',
                'company': company.text.strip() if company else '',
                'location': location.text.strip() if location else '',
                'link': link
            })
        print(jobs)
    else:
        jobs.append({'error': f'Failed to fetch jobs from Naukri. Status code: {response.status_code}'})
    return jobs 