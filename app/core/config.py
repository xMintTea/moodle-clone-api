from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
from env2 import env2

load_dotenv()

class Config(BaseSettings):
    app_name: str = "MoodleClone"
    debug: bool = False
    
    jwt_private_key_path: Path = Path(env2("JWT_PRIVATE_KEY_PATH")) #type: ignore
    jwt_public_key_path: Path = Path(env2("JWT_PUBLIC_KEY_PATH")) #type: ignore
    jwt_algorithm: str = env2("JWT_ALG") # type: ignore
    jwt_access_expire_minutes: int = env2("JWT_ACCESS_EXPIRE_MINS")  #type: ignore
    jwt_refresh_expire_days: int = env2("JWT_REFRESH_EXPIRE_DAYS")  #type: ignore
    
    db_url: str = env2("DATABASE_URL") #type: ignore



config = Config()
