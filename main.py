from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def greet():
    return "WELCOME TO 3 ASGI FASAPI COURSE ENROLLMENT SYSTEM"
