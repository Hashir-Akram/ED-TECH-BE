import httpx
import json

def stream_ollama_response(prompt):
    url = "http://localhost:11434/api/generate"
    model = "gemma"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }

    response_text = ""

    try:
        with httpx.stream("POST", url, json=payload, timeout=60.0) as response:
            response.raise_for_status()

            # Handle each JSON line
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            chunk = data["response"]
                            response_text += chunk
                            print(chunk, end='', flush=True)  # Stream it live in terminal
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        print("❌ JSON decode error:", line)

    except Exception as e:
        print("❌ Error:", str(e))

    return response_text


# Test it
query = "Devops"
prompt = f"""
You are an EdTech AI assistant. A user is interested in "{query}".

Here are some relevant courses and lessons:
Courses:
DevOps

Lessons:
Introduction to devops

Based on this, briefly suggest a personalized learning path to master the topic.
"""
full_response = stream_ollama_response(prompt)
print("\n\n✅ Final response:\n", full_response)
