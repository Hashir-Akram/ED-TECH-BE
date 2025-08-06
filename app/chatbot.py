# app/routes/chatbot.py

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app import database, models
from app.llm_engine import ask_llm

router = APIRouter(tags=["Chatbot"])

@router.get("/chatbot")
def chatbot(query: str = Query(...), db: Session = Depends(database.get_db)):
    courses = db.query(models.Course).all()
    lessons = db.query(models.Lesson).all()

    course_data = "\n".join([f"- {c.title}: {c.description}" for c in courses])
    lesson_data = "\n".join([f"- {l.title} (in {l.course.title})" for l in lessons if l.course])

    prompt = f"""
You are a helpful learning assistant. Based on the following available courses and lessons, answer the user's query: "{query}"

Available courses:
{course_data}

Available lessons:
{lesson_data}

Respond clearly and helpfully.
"""

    reply = ask_llm(prompt)
    return {"response": reply}
