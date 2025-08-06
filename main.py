from fastapi import FastAPI
from app import models, database
from app.auth import router as auth_router
from app.courses import router as course_router
from app.lessons import router as lesson_router
from app.recommendations import router as recommend_router
from app.chatbot import router as chatbot
from fastapi.middleware.cors import CORSMiddleware




models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="EdTech Platform")


# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(course_router, prefix="/courses")
app.include_router(lesson_router)
app.include_router(recommend_router)
app.include_router(chatbot)


@app.get("/")
def home():
    return {"message": "EdTech API is running"}
