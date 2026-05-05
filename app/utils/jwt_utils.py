import jwt
from datetime import datetime, timezone, timedelta
from typing import Optional

from ..models.user import User
from ..core.config import config

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


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



def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = config.jwt_access_expire_minutes,
    expire_timedelta: Optional[timedelta] = None) -> str:
    
    now = datetime.now(timezone.utc)
    
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    
    jwt_payload = {
        TOKEN_TYPE_FIELD: token_type,
        "iat" : now,
        "exp" : expire
        }
    
    jwt_payload.update(token_data)
    
    return encode_jwt(jwt_payload)

def create_access_token(user: User) -> str:
    jwt_payload = {
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "email" : user.email,
        "role" : user.user_type
    }
    
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload
    )
    
def create_refresh_token(user: User) -> str:
    jwt_payload = {
        "sub" : user.email
    }
    
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta= timedelta(days=config.jwt_refresh_expire_days)
    )