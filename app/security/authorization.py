from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Security
from sqlalchemy.orm import Session
from pydantic import EmailStr

from .security import bearer_schema
from ..utils import jwt_utils
from ..service.user_service import UserService
from ..database import get_db
from ..models.user import User


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


def get_payload_user(credentials: HTTPAuthorizationCredentials = Security(bearer_schema)):
    token = credentials.credentials
    
    return jwt_utils.decode_jwt(token)



def get_user(
    payload: dict = Depends(get_payload_user),
    user_service: UserService = Depends(get_user_service)
    ) -> User:
    user_email = payload.get("email")
    
    if not user_email:
        raise ValueError
    
    user = user_service.get_user_by_email(user_email)
    
    if not user:
        raise ValueError
    
    return user


def is_user_allow_test(
    user: User = Depends(get_user)
):
    return True