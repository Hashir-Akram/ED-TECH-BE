# llm_engine.py

import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma"  # Replace with "phi", "llava", etc., if desired

def generate_feedback(question: str, answer: str, model: str = DEFAULT_MODEL) -> str:
    prompt = f"""
You are an educational AI tutor.

Evaluate the student's answer and provide constructive feedback.

If the answer is wrong, correct it and explain why.

Question: {question}
Student's Answer: {answer}
Feedback:
"""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = httpx.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["response"].strip()
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP error {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        print(f"❌ Request error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return "⚠️ Couldn't get feedback from the AI."
