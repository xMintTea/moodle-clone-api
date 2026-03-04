from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from models.user import User
from schemas.user import UserSchema
from utils import password as pw_utils


class UserService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    
    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        stmt = select(User).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())
    
    def get_user(self, user_id: int) -> User | None:
        return self._db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, user_schema: UserSchema) -> User:
        
        user = User(**user_schema.model_dump())
        user.password = pw_utils.hash_password(user_schema.password)
        
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update_user(self, user_id: int, user_schema: UserSchema) -> User:
        user = self._get_user_or_raise(user_id)
        
        user.first_name = user_schema.first_name
        user.middle_name = user_schema.middle_name
        user.last_name = user_schema.last_name
        user.email = user_schema.email
        user.user_status = user_schema.user_status
        user.user_type = user_schema.user_type
            
        if not pw_utils.validate_password(user_schema.password, user.password):
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