from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Security, status, Form, Response, Request, Cookie
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from pydantic import EmailStr
from fastapi.exceptions import HTTPException

from .security import bearer_scheme, oauth2_scheme
from ..utils import jwt_utils
from ..service.user_service import UserService
from ..database import get_db
from ..models.user import User
from ..models.context.enums import UserStatus
from ..utils.jwt_utils import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from ..schemas.auth import Token


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


def get_payload(
        token: str = Depends(oauth2_scheme)
    ):
    
    return jwt_utils.decode_jwt(token)


def validate_token_type(payload: dict, token_type: str):
    current_token_type = payload.get("type")
    if current_token_type == token_type:
        return True
    
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type {current_token_type!r} expected {token_type!r}"    
        )



def get_verified_user(
    payload: dict = Depends(get_payload),
    user_service: UserService = Depends(get_user_service)
    ) -> User:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    
    user_email = payload.get("email")
    
    if not user_email:
        raise ValueError
    
    user = user_service.get_user_by_email(user_email)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    if user.user_status == UserStatus.SUSPENDED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return user


def login_user_dependency():
    def dependency(
        response: Response,
        username: EmailStr = Form(),
        password: str = Form(),
        user_service: UserService = Depends(get_user_service)
    ):
        
        tokens = user_service.login_user(username, password)
        
        if tokens.refresh_token is None:
            return

        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
            max_age=10*60*24
        )
        
        return tokens
    return dependency


def refresh_access_token_dependency():
    def dependency(
        response: Response,
        refresh_token = Cookie(None),
        user_service: UserService = Depends(get_user_service)
    ) -> Token:
        
        if refresh_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        payload = get_payload(refresh_token)
        validate_token_type(payload, REFRESH_TOKEN_TYPE)
        
        new_tokens = user_service.refresh_user_token(payload)
        
        
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
            max_age=10*60*24
        )
        
        
        return new_tokens
        
    return dependency