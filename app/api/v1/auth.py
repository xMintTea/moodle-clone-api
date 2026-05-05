from fastapi import Depends, status, Form
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from pydantic import EmailStr

from ...service.user_service import UserService
from ...schemas.auth import Token
from ...database import get_db
from ...schemas.user import UserResponse, UserCreate
from ...models.user import User
from ...security.authorization import refresh_access_token_dependency

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
    

@router.post(
    "/login",
    response_model=Token,
    response_model_exclude_none=True
    )
def login(
    username: EmailStr = Form(),
    password: str = Form(),
    user_service: UserService = Depends(get_user_service)
) -> Token:
    return user_service.login_user(username, password)


@router.post("/refresh", response_model=Token, response_model_exclude_none=True)
def refresh_jwt(
    token: Token = Depends(refresh_access_token_dependency())
):
    return token