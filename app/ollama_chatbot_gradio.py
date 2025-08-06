import gradio as gr
import httpx
import json

# Ollama server URL and model
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma"  # Change to 'phi', 'llama3', etc. if needed

# Streaming response generator from Ollama
def stream_ollama(prompt):
    try:
        with httpx.stream("POST", OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": True
        }, timeout=60.0) as response:
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        token = data.get("response", "")
                        yield token
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        yield f"❌ Error: {str(e)}"

# Chat handler for Gradio
def chat(user_input, history):
    history = history or []
    full_prompt = "\n".join([f"User: {msg[0]}\nAI: {msg[1]}" for msg in history])
    full_prompt += f"\nUser: {user_input}\nAI:"

    response_stream = stream_ollama(full_prompt)

    bot_response = ""
    for chunk in response_stream:
        bot_response += chunk
        yield history + [[user_input, bot_response]]

# Gradio UI setup
with gr.Blocks(title="Ollama Chatbot") as demo:
    gr.Markdown("## 💬 Local AI Chatbot (Ollama + Gradio)")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask something...", label="Your Message")
    clear = gr.Button("Clear Chat")

    state = gr.State([])

    msg.submit(chat, inputs=[msg, state], outputs=[chatbot], show_progress=True).then(
        lambda x: "", None, msg
    )
    clear.click(lambda: ([], []), None, outputs=[chatbot, state])

# Launch app
if __name__ == "__main__":
    demo.launch()
