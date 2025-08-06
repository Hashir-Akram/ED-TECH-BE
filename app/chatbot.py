from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app import database, models
from app.llm_engine import ask_llm

router = APIRouter(tags=["Chatbot"])

@router.get("/chatbot")
def chatbot(query: str = Query(...), db: Session = Depends(database.get_db)):
    # Fetching course and lesson data
    courses = db.query(models.Course).all()
    lessons = db.query(models.Lesson).all()

    # Convert DB into clean, natural text
    course_data = "\n".join([f"- {c.title}: {c.description}" for c in courses])
    lesson_data = "\n".join([f"- {l.title} (in {l.course.title})" for l in lessons if l.course])

    # Constructing a more focused, professional prompt for the LLM
    prompt = f"""
You are a helpful learning assistant. Based on the following available courses and lessons, suggest a learning path for the user:

Available courses:
{course_data}

Available lessons:
{lesson_data}

The user is interested in learning about: "{query}"

Provide a concise and professional suggestion for a learning path to become proficient in the topic of interest, including the key topics or resources to focus on.
"""

    # Get the response from LLM (assuming ask_llm is a function that handles LLM interaction)
    reply = ask_llm(prompt)

    # Returning the cleaned response
    return {"response": reply.strip()}
