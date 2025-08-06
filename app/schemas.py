from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "student"

class LoginRequest(BaseModel):
    email: str
    password: str
    

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CourseCreate(BaseModel):
    title: str
    description: str
    price: float


class CourseOut(CourseCreate):
    id: int
    instructor_id: int

    class Config:
        orm_mode = True


class LessonCreate(BaseModel):
    title: str
    video_url: str
    question: str  # NEW

class LessonOut(LessonCreate):
    id: int
    course_id: int

    class Config:
        orm_mode = True
