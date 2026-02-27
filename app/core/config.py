from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    app_name: str = "MoodleClone"
    debug: bool = False
    db_name: str = "project.db"
    
    @property
    def db_url(self):
        return f"sqlite:///./{self.db_name}"



config = Config()
