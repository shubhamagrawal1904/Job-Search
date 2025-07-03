import os
from dotenv import load_dotenv
import json

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Add more providers as needed
def get_llm():
    with open('config.json', 'r') as f:
        config = json.load(f)
    llm_name = config.get('llm_name', 'groq')
    llm_model = config.get('llm_model', 'deepseek-r1-distill-llama-70b')
    if llm_name.lower() == 'groq':
        from langchain_groq import ChatGroq
        return ChatGroq(api_key=GROQ_API_KEY, model=llm_model)
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_name}") 