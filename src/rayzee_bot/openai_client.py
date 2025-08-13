import os
from typing import Optional, List
import requests

# Minimal HTTP client placeholder; replace with official SDK if preferred.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
OPENAI_BASE = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}

def draft_tweet(system_prompt: str, user_prompt: str, max_tokens: int = 120, temperature: float = 0.7):
    data = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    r = requests.post(OPENAI_BASE, json=data, headers=HEADERS, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def describe_image_stub(image_url: str) -> str:
    # TODO: Call multimodal endpoint to extract description/tags
    return "placeholder description of the image (TODO: integrate vision API)"
