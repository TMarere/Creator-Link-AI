from fastapi import FastAPI
from app.db.database import Base, engine
from app.db.models import users  # noqa: F401



Base.metadata.create_all(bind=engine)

app = FastAPI(title="CreatorAI Link")
@app.get("/")
def root():


    return {"message": "CreatorLink AI backend is running"}

