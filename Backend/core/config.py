import os


class Settings:
    def __init__(self) -> None:
        # Defaults let the app boot even when .env is missing.
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./creatorlink.db")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


settings = Settings()




    
