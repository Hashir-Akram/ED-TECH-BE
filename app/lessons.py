# app/routes/lessons.py

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app import database, models, schemas
from app.ai_feedback import generate_feedback

router = APIRouter(tags=["Lessons"])

# -------------------------------
# Create a new lesson for a course
# -------------------------------
@router.post("/courses/{course_id}/lessons", response_model=schemas.LessonOut)
def create_lesson(course_id: int, lesson: schemas.LessonCreate, db: Session = Depends(database.get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    new_lesson = models.Lesson(**lesson.dict(), course_id=course_id)
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

# -------------------------------
# Get all lessons for a course
# -------------------------------
@router.get("/courses/{course_id}/lessons", response_model=list[schemas.LessonOut])
def get_lessons(course_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Lesson).filter(models.Lesson.course_id == course_id).all()

# -------------------------------
# Submit student's answer and get AI feedback
# -------------------------------
@router.post("/lessons/{lesson_id}/submit-answer")
def submit_answer(
    lesson_id: int,
    student_answer: str = Body(..., embed=True),
    db: Session = Depends(database.get_db)
):
    # Fetch the lesson and ensure it exists
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if not lesson.question:
        raise HTTPException(status_code=400, detail="This lesson has no question to evaluate.")

    # Call AI model to generate feedback
    feedback = generate_feedback(lesson.question, student_answer)

    # Respond with structured feedback
    return {
        "lesson_id": lesson.id,
        "question": lesson.question,
        "student_answer": student_answer,
        "feedback": feedback
    }
