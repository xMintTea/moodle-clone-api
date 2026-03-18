from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import Optional

from ..schemas.course_user import CreateCourseUser, UpdateCourseUser
from ..models.course import CourseUser, User
from ..models.context.enums import UserType

class CourseUserService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    
    def list_records(self, skip: int = 0, limit: int = 100) -> list[CourseUser]:
        stmt = select(CourseUser).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())
    
    
    def get_record(self, record_id: int) -> Optional[CourseUser]:
        return self._db.get(CourseUser, record_id)


    def list_records_in_course(self, course_id: int) -> list[CourseUser]:
        stmt = select(CourseUser).filter(CourseUser.course_id == course_id)
        return list(self._db.scalars(stmt).all())

    def list_students_in_course(self, course_id: int) -> list[User]:
        return self._list_users_by_role_id(course_id, UserType.DEFAULT)


    def list_teachers_in_course(self, course_id: int) -> list[User]:
        return self._list_users_by_role_id(course_id, UserType.REDACTOR)


    def list_admins_in_course(self, course_id: int) -> list[User]:
        return self._list_users_by_role_id(course_id, UserType.ADMIN)
    
    
    def add_record(self,course_id: int, courseuser_data: CreateCourseUser) -> CourseUser:
        course_user = CourseUser(**courseuser_data.model_dump()) 
        course_user.course_id = course_id
        
        self._db.add(course_user)
        self._db.commit()
        self._db.refresh(course_user)
        
        return course_user
    
    
    def update_record(self, record_id: int, record_data: UpdateCourseUser) -> CourseUser:
        record = self._get_record_or_raise(record_id)
        update_dict = record_data.model_dump(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(record, field, value)
        
        self._db.commit()
        self._db.refresh(record)
        
        return record
    
    
    def delete_record(self, record_id: int):
        record = self._get_record_or_raise(record_id)
        
        self._db.delete(record)
        self._db.commit()
        
    
    def _list_users_by_role_id(self, course_id: int, role_id: int):
        stmt = select(CourseUser) \
        .filter(CourseUser.course_id == course_id) \
        .filter(CourseUser.access_level == role_id)
        
        course_users = self._db.scalars(stmt).all()
        users = [course_user.user for course_user in course_users]
        
        return users
    
    
    def _get_record_or_raise(self, record_id: int) -> CourseUser:
        record = self.get_record(record_id)
        
        if not record:
            raise NoResultFound
        
        return record