from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Config(BaseSettings):
    app_name: str = "MoodleClone"
    debug: bool = False
    
    @property
    def db_url(self) -> str:
        url = os.getenv("DATABASE_URL")
        if url is None:
            raise ValueError("DATABASE_URL environment variable not set")
        return url



config = Config()
