from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import Optional

from ..models.course import SectionPage, SubmittedPage
from ..models.file import File
from ..schemas.pages import PageCreate, PageUpdate
from ..schemas.submission import PageSubmissionCreate, PageSubmissionUpdate

class PageService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    
    def list_pages(self, skip: int = 0, limit: int = 100) -> list[SectionPage]:
        stmt = select(SectionPage).offset(skip).limit(limit)
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
        
        update_dict = page_schema.model_dump(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(page, field, value)

        page.last_change_date = datetime.now()

        self._db.commit()
        self._db.refresh(page)
        
        return page


    def delete_page(self, page_id: int):
        page = self._get_page_or_raise(page_id)
        
        self._db.delete(page)
        self._db.commit()


    def get_submittion(self, submittion_id: int) -> Optional[SubmittedPage]:
        stmt = select(SubmittedPage).filter(SubmittedPage.id == submittion_id)
        return self._db.scalar(stmt)
    
    
    def get_submittions(
        self,
        page_id: Optional[int] = None,
        user_id: Optional[int] = None
        ) -> list[SubmittedPage]:

        stmt = select(SubmittedPage)
        
        if user_id:
            stmt = stmt.filter(SubmittedPage.user_id == user_id)
        
        if page_id:
            stmt = stmt.filter(SubmittedPage.page_id == page_id)

        return list(self._db.scalars(stmt).all())
    
    
    def create_submittion(self,page_id, submittion_data: PageSubmissionCreate) -> SubmittedPage:
        submitted_page: SubmittedPage = SubmittedPage(**submittion_data.model_dump())
        submitted_page.page_id = page_id
        
        self._db.add(submitted_page)
        self._db.commit()
        self._db.refresh(submitted_page)
        
        return submitted_page
    
    
    def update_submittion(self, submittion_id: int, submittion_data: PageSubmissionUpdate) -> SubmittedPage:
        submittion = self._get_submittion_or_raise(submittion_id)
        
        update_dict = submittion_data.model_dump(exclude_unset=True)
        
        for key, value in update_dict.items():
            setattr(submittion, key, value)
            
        self._db.commit()
        self._db.refresh(submittion)
        
        return submittion
        
    
    
    def add_file_to_page(self, page_id: int, file_id: int) -> SectionPage:
        page = self._get_page_or_raise(page_id)
        file = self._get_file_or_raise(file_id)
        
        page.files.append(file)
        
        self._db.commit()
        self._db.refresh(page)
        
        return page
    
    
    def add_file_to_submittion(self, submittion_id: int, file_id: int) -> SubmittedPage:
        submittion = self._get_submittion_or_raise(submittion_id)
        file = self._get_file_or_raise(file_id)
        
        submittion.files.append(file)
        
        self._db.commit()
        self._db.refresh(submittion)
        
        return submittion
    
    
    
    def _get_file_or_raise(self, file_id: int) -> File:
        file = self._db.get(File, file_id)
        
        if not file:
            raise NoResultFound
        
        return file
    
    
    def _get_page_or_raise(self, page_id: int) -> SectionPage:
        page = self.get_page(page_id)
        if not page:
            raise NoResultFound
        return page
    
    
    def _get_submittion_or_raise(self, submittion_id: int) -> SubmittedPage:
        submittion = self.get_submittion(submittion_id)

        if not submittion:
            raise NoResultFound
        
        return submittion
    
    