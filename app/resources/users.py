from fastapi import Depends, status, Query, Path
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from typing import Optional, Annotated
from sqlalchemy.orm import Session

from ..service.user_service import UserService
from ..database import get_db
from ..models.user import User
from ..models.context.enums import UserType
from ..schemas.user import UserResponse, UserCreate, UserUpdate
from ..security.authorization import get_verified_user


def get_user_service(session: Session = Depends(get_db)) -> UserService:
    return UserService(session)


def get_users_dependency():
    def dependency(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        group_name: Optional[str] = Query(None),
        user_service: UserService = Depends(get_user_service),
        user: User = Depends(get_verified_user)
        ) -> list[User]:
        return user_service.list_users(skip,limit, group_name)

    return dependency


def get_user_dependency():
    def dependency(
        user_id: Annotated[int, Path(ge=1)],
        user_service: UserService = Depends(get_user_service),
        user: User = Depends(get_verified_user)
        ) -> Optional[User]:
        return user_service.get_user(user_id)

    return dependency


def update_user_dependency():
    def dependency(
        user_id: Annotated[int, Path(ge=1)],
        user_data: UserUpdate,
        user_service: UserService = Depends(get_user_service),
        user: User = Depends(get_verified_user)
        ) -> User:
        
        if user.user_type == UserType.ADMIN:
            return user_service.update_user(user_id, user_data)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return dependency


def delete_user_dependency():
    def dependency(
        user_id: Annotated[int, Path(ge=1)],
        user_service: UserService = Depends(get_user_service),
        user: User = Depends(get_verified_user)
    ):
        
        if user.user_type == UserType.ADMIN:
            user_service.delete_user(user_id)
            
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
    return dependency