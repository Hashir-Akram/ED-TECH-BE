from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load only once
model_name = "microsoft/phi-2"  # Or mistral-7B if you have resources
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)

def ask_llm(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=100, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt, "").strip()
