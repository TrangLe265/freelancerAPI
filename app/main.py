from fastapi import FastAPI

app = FastAPI(titlle="Freelancer API", version="1.0.0")

@app.get("/")
def health_check():
    return {"status": "ok"}