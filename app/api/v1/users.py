from fastapi import Depends, status, Query
from fastapi.routing import APIRouter
from typing import Optional
from sqlalchemy.orm import Session

from ...service.user_service import UserService
from ...database import get_db
from ...models.user import User
from ...schemas.user import UserResponse, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(session: Session = Depends(get_db)) -> UserService:
    return UserService(session)


@router.get("/", response_model=list[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_service: UserService = Depends(get_user_service)
    ) -> list[User]:
    return user_service.list_users(skip,limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
    ) -> Optional[User]:
    return user_service.get_user(user_id)

@router.post("/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
    )
def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
    ) -> User:
    return user_service.create_user(user_data)

@router.put("/{user_id}",
    response_model=UserResponse
    )
def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
    ) -> User:
    return user_service.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    )
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    user_service.delete_user(user_id)