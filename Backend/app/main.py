from fastapi import FastAPI

app = FastAPI(title ="CreatorAI Link")
@app.get("/")
def root():


    return {"message": "CreatorLink AI backend is running"}