import jwt
from datetime import datetime, timezone, timedelta

from ..models.user import User
from ..core.config import config

def encode_jwt(
    payload: dict,
    private_key: str = config.jwt_private_key_path.read_text(),
    algorithm: str = config.jwt_algorithm
    ):
    encoded = jwt.encode(payload, private_key, algorithm)
    
    return encoded

def decode_jwt(
    token: str | bytes,
    public_key: str = config.jwt_public_key_path.read_text(),
    algorithm: str = config.jwt_algorithm
    ):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    
    return decoded

def create_payload(user: User) -> dict:
    
    now = datetime.now(timezone.utc)
    
    jwt_payload = {
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "email" : user.email,
        "type" : user.user_type,
        "iat" : now,
        "exp" : now + timedelta(minutes=15) #TODO: вынести в настройки
    }
    
    return jwt_payload