from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from models.course import Course
from schemas.course import CourseSchema


class CourseService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    def list_courses(self, skip: int = 0, limit: int = 100) -> list[Course]:
        return self._db.query(Course).offset(skip).limit(limit).all()
    
    
    
    def get_course(self, course_id: int) -> Course | None:
        return self._db.query(Course).filter(Course.id == course_id).first()
    
    
    def add_course(self, course_schema: CourseSchema) -> Course:
        course = Course(**course_schema.model_dump())
        
        self._db.add(course)
        self._db.commit()
        self._db.refresh(course)
        
        return course

    def update_course(self, course_id: int, course_schema: CourseSchema) -> Course:
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