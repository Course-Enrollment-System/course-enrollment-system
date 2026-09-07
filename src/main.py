from fastapi import FastAPI

from src.config.database import Base, engine
from src.config.init_db import init_db
from src.routers.student_router import router as student_router
from src.routers.course_router import router as course_router
from src.routers.auth_router import router as auth_router
from src.routers.enrollment_router import router as enrollment_router

# please for the love of god start the server with "uv run uvicorn src.main:app --reload"

init_db()
app = FastAPI(title="Course Enrollment System")

app.include_router(student_router)
app.include_router(course_router)
app.include_router(auth_router)
app.include_router(enrollment_router)

Base.metadata.create_all(bind=engine)




