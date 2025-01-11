import requests

from config import Config

API_KEY = Config.ANTHROPIC_API_KEY
url = "https://api.anthropic.com/v1/complete"


def chat_with_claude(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "claude-1",  # Adjust based on the specific Claude model
        "prompt": prompt,
        "max_tokens": 150,
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    return data['completion']
