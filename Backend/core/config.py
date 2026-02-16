from pydantic import BaseSettings
class settings(BaseSettings):
    DATABASE_URL: str
    SECTET_KEY: str

class Config:
    env_file = ".env"

    settings = settings(_env_file=".env")




    