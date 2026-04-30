from fastapi import Depends, status, Query, Form, Security
from fastapi.routing import APIRouter
from typing import Optional
from sqlalchemy.orm import Session
from pydantic import EmailStr
from fastapi.security import HTTPBearer

from ...service.user_service import UserService
from ...schemas.auth import Token
from ...database import get_db
from ...schemas.user import UserResponse, UserCreate
from ...models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])




def get_user_service(session: Session = Depends(get_db)) -> UserService:
    return UserService(session)


@router.post("/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
    )
def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
    ) -> User:
    return user_service.create_user(user_data)
    

@router.post("/login", response_model=Token)
def login(
    email: EmailStr = Form(),
    password: str = Form(),
    user_service: UserService = Depends(get_user_service)
) -> Token:
    return user_service.login_user(email, password)



from ...security.authorization import is_user_allow_test

bearer = HTTPBearer()

@router.get("/test")
def test(
    user: User = Depends(is_user_allow_test)
):
    return user