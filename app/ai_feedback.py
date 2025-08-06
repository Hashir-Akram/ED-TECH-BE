from transformers import pipeline

# Load the model for text generation
feedback_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

def generate_feedback(question: str, answer: str) -> str:
    # Construct a prompt to ask the AI to validate the answer and suggest improvements
    prompt = f"Given the question below, evaluate the user's answer and provide constructive feedback. If the answer is incorrect, provide the correct answer and suggest improvements.\n\nQuestion: {question}\nUser Answer: {answer}\nFeedback:"

    # Get the feedback from the model
    result = feedback_pipeline(prompt, max_length=200)[0]['generated_text']

    # Return the stripped feedback text
    return result.strip()

# Example usage
question = "What is the capital of France?"
user_answer = "Berlin"

feedback = generate_feedback(question, user_answer)
print(feedback)
