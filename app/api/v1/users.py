from fastapi import Depends, status, Query, Path
from fastapi.routing import APIRouter
from typing import Optional

from ...models.user import User
from ...schemas.user import UserResponse
from ...resources.users import (
    get_users_dependency,
    get_user_dependency,
    update_user_dependency,
    delete_user_dependency
)


router = APIRouter(prefix="/users", tags=["Users"])



@router.get("/", response_model=list[UserResponse])
def get_users(
    users: list[User] = Depends(get_users_dependency())
    ) -> list[User]:
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user: Optional[User] = Depends(get_user_dependency())
    ) -> Optional[User]:
    return user


@router.put("/{user_id}",
    response_model=UserResponse
    )
def update_user(
    user: User = Depends(update_user_dependency())
    ) -> User:
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    )
def delete_user(
    _ = Depends(delete_user_dependency())
):
    ...