import os
import requests
from dotenv import load_dotenv

# Load the API key from an environment variable
load_dotenv()
hf_token = os.getenv('API_KEY')
headers = {"Authorization": f"Bearer {hf_token}"}

# Define the model ID
model_id = "sentence-transformers/all-MiniLM-L6-v2"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"

def get_embedding(chunk):
    response = requests.post(api_url, headers=headers, json={"inputs": chunk, "options": {"wait_for_model": True}})
    response_json = response.json()
    embedding = response_json[0]
    return embedding



