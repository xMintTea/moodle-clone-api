from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import Optional

from ..models.course import SectionPage
from ..schemas.course import PageCreate, PageUpdate

class PageService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    
    def list_pages(self, section_id: int, skip: int = 0, limit: int = 100) -> list[SectionPage]:
        stmt = select(SectionPage) \
            .filter(SectionPage.section_id == section_id)\
            .offset(skip)\
            .limit(limit)
        return list(self._db.scalars(stmt).all())



    def get_page(self, page_id: int) -> Optional[SectionPage]:
        return self._db.get(SectionPage, page_id)


    def create_page(self, page_schema: PageCreate) -> SectionPage:
        page = SectionPage(**page_schema.model_dump())
        self._db.add(page)
        self._db.commit()
        self._db.refresh(page)
        
        return page
    
    
    def update_page(self, page_id: int, page_schema: PageUpdate) -> SectionPage:
        page = self._get_page_or_raise(page_id)
        
        page.section_id = page_schema.section_id
        page.order = page_schema.order
        page.visibility_id = page_schema.visibility_id
        page.last_change_date = datetime.now()

        self._db.commit()
        self._db.refresh(page)
        
        return page


    def delete_page(self, page_id: int):
        page = self._get_page_or_raise(page_id)
        
        self._db.delete(page)
        self._db.commit()
    
    
    def _get_page_or_raise(self, page_id) -> SectionPage:
        page = self.get_page(page_id)
        if not page:
            raise NoResultFound
        return page
    
    
    
    
    