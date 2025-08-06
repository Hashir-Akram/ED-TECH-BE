from fastapi import APIRouter, Depends, HTTPException, Path,Body
from sqlalchemy.orm import Session
from app import database, models, schemas
from app.ai_feedback import generate_feedback

router = APIRouter(tags=["Lessons"])

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

@router.get("/courses/{course_id}/lessons", response_model=list[schemas.LessonOut])
def get_lessons(course_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Lesson).filter(models.Lesson.course_id == course_id).all()


@router.post("/lessons/{lesson_id}/submit-answer")
def submit_answer(lesson_id: int, student_answer: str = Body(..., embed=True), db: Session = Depends(database.get_db)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    feedback = generate_feedback(lesson.question, student_answer)
    return {"feedback": feedback}