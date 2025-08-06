from fastapi import APIRouter

router = APIRouter(tags=["Recommendations"])

@router.get("/recommend")
def recommend_courses():
    return [
        {"id": 1, "title": "Python for Kids", "score": 0.95},
        {"id": 2, "title": "Learn HTML", "score": 0.90},
        {"id": 3, "title": "Fun with Scratch", "score": 0.88}
    ]
