from fastapi import FastAPI

app = FastAPI()

app.include_router(router)

@app.get("/")
def greet():
    return "WELCOME TO 3 ASGI FASAPI COURSE ENROLLMENT SYSTEM"
