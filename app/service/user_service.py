from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import Optional
from pydantic import EmailStr

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..schemas.auth import Login, Token
from ..utils import password as pw_utils
from ..utils import jwt_utils


class UserService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    
    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        stmt = select(User).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self._db.get(User, user_id)
    
    def get_user_by_email(self, user_email: EmailStr) -> Optional[User]:
        stmt = select(User).filter(User.email == user_email)
        return self._db.scalar(stmt)
    
    def create_user(self, user_schema: UserCreate) -> User:
        
        user = User(**user_schema.model_dump())
        user.password = pw_utils.hash_password(user_schema.password)
        
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update_user(self, user_id: int, user_schema: UserUpdate) -> User:
        user = self._get_user_or_raise(user_id)
        

        update_dict = user_schema.model_dump(exclude_unset=True)
        
        
        for field, value in update_dict.items():
            setattr(user, field, value)

            
        if "password" in update_dict.keys():
            user.password = pw_utils.hash_password(user_schema.password)
            
        self._db.commit()
        self._db.refresh(user)
        return user
    

    
    def delete_user(self, user_id: int):
        user = self._get_user_or_raise(user_id)
        self._db.delete(user)
        self._db.commit()

    def _get_user_or_raise(self, user_id: int) -> User:
        user = self.get_user(user_id)
        if not user:
            raise NoResultFound
        
        return user
    
    
    
    def login_user(self, email: EmailStr, password: str) -> Token:
        user = self.get_user_by_email(email)
        if not user:
            raise NoResultFound #TODO: Не найдено -> Неверный логин/пароль
        
        matched_pw = pw_utils.validate_password(password, user.password)
        
        if not matched_pw:
            raise NoResultFound #TODO: Неверный логин/пароль
        

        access_token = jwt_utils.create_access_token(user)
        refresh_token = jwt_utils.create_refresh_token(user)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
        
    def refresh_user_token(self, payload: dict) -> Token:
        email: EmailStr = payload.get("sub")  #type: ignore
        
        user = self.get_user_by_email(email)
        
        if user is None:
            raise NoResultFound
        
        fresh_access_token = jwt_utils.create_access_token(user)
        
        return Token(access_token=fresh_access_token)