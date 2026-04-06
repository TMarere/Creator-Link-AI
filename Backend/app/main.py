from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.db.models import users  # noqa: F401
from app.api.v1.connections import router as connections_router
from app.api.v1.recommendations import router as recommendations_router
from app.api.v1.users import router as users_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="CreatorAI Link")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(users_router)
app.include_router(recommendations_router)
app.include_router(connections_router)


@app.get("/")
def root():

    return {"message": "CreatorLink AI backend is running"}
