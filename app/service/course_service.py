from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import Optional

from ..models.course import Course
from ..schemas.course import CourseCreate, CourseUpdate


class CourseService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    def list_courses(self, skip: int = 0, limit: int = 100) -> list[Course]:
        stmt = select(Course).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())

    
    def get_course(self, course_id: int) -> Optional[Course]:
        return self._db.get(Course, course_id)
    
    
    def create_course(self, course_schema: CourseCreate) -> Course:
        course = Course(**course_schema.model_dump())
        
        self._db.add(course)
        self._db.commit()
        self._db.refresh(course)
        
        return course

    def update_course(self, course_id: int, course_schema: CourseUpdate) -> Course:
        course = self._get_course_or_raise(course_id)
        course.name = course_schema.name
        course.description = course_schema.description
        course.secret = course_schema.secret
        course.visibility_id = course_schema.visibility_id
        
        self._db.commit()
        self._db.refresh(course)
        
        return course
    
    
    def delete_course(self, course_id: int):
        course = self._get_course_or_raise(course_id)
        self._db.delete(course)
        self._db.commit()

    
    def _get_course_or_raise(self, course_id: int) -> Course:
        course = self.get_course(course_id)
        if not course:
            raise NoResultFound
        return course