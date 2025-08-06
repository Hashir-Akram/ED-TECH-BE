# app/llm_engine.py

import httpx
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma"  # Change this to 'phi' or other model if needed

def ask_llm(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True
    }

    full_response = ""

    try:
        with httpx.stream("POST", OLLAMA_URL, json=payload, timeout=60.0) as response:
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        token = data.get("response", "")
                        full_response += token
                    except json.JSONDecodeError:
                        continue

        return full_response.strip()

    except Exception as e:
        print(f"[Ollama LLM ERROR] {e}")
        return "⚠️ Could not get a response from the AI."
