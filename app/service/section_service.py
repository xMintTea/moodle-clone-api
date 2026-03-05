from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import Optional

from ..models.course import CourseSection
from ..schemas.course import SectionCreate, SectionUpdate

class SectionService:
    def __init__(self, session: Session):
        self._db = session
    
    
    def list_sections(self, skip: int = 0, limit: int = 100) -> list[CourseSection]:
        stmt = select(CourseSection).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())
    
    
    def get_section(self, section_id: int) -> Optional[CourseSection]:
        return self._db.get(CourseSection, section_id)
    
    
    def create_section(self, section_schema: SectionCreate) -> CourseSection:
        section = CourseSection(**section_schema.model_dump())
        self._db.add(section)
        self._db.commit()
        self._db.refresh(section)
        
        return section
    
    
    def update_section(self,section_id: int, section_schema: SectionUpdate) -> CourseSection:
        section = self._get_section_or_raise(section_id)
        
        section.title = section_schema.title
        section.description = section_schema.description
        section.order = section_schema.order
        section.visibility_id = section_schema.visibility_id
        section.course_id = section_schema.course_id

        
        self._db.commit()
        self._db.refresh(section)
        
        return section
    
    def delete_section(self, section_id: int):
        section = self._get_section_or_raise(section_id)
        self._db.delete(section)
        self._db.commit()
    
    def _get_section_or_raise(self, section_id: int) -> CourseSection:
        section = self.get_section(section_id)
        if not section:
            raise NoResultFound
        return section