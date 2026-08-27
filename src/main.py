from fastapi import FastAPI
from src.routers.student_router import router as student_router

# please for the love of god start the server with "uv run uvicorn src.main:app --reload"
app = FastAPI()

app.include_router(student_router)