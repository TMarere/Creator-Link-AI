from fastapi import FastAPI
from app.routers import users
from Backend.app.db.database import Base, engine



Base.metadata.create_all(bind=engine)

app = FastAPI(title ="CreatorAI Link")
@app.get("/")
def root():


    return {"message": "CreatorLink AI backend is running"}


