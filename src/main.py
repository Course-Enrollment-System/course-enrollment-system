from fastapi import FastAPI

from src.config.database import engine
from src.routers.student_router import router as student_router
from src.routers.course_router import router as course_router
from src.config.init_db import Base

# please for the love of god start the server with "uv run uvicorn src.main:app --reload"

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(student_router)
app.include_router(course_router)