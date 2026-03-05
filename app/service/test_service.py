from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import Optional

from ..models.course import Test
from ..schemas.course import TestCreate, TestUpdate

class TestService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    
    def list_tests(self, section_id: int, skip: int = 0, limit: int = 100) -> list[Test]:
        stmt = select(Test)\
                .filter(Test.section_id == section_id)\
                .offset(skip)\
                .limit(limit)
        
        return list(self._db.scalars(stmt).all())


    def get_test(self, test_id: int) -> Optional[Test]:
        return self._db.get(Test, test_id)
    
    
    def create_test(self, test_schema: TestCreate) -> Test:
        test = Test(**test_schema.model_dump())
        
        self._db.add(test)
        self._db.commit()
        self._db.refresh(test)
        
        return test


    def update_test(self, test_id: int, test_schema: TestUpdate) -> Test:
        test = self._get_test_or_raise(test_id)
        
        test.section_id = test_schema.section_id
        test.deadline_date = test_schema.deadline_date
        test.order = test_schema.order
        test.visibility_id = test_schema.visibility_id
        test.last_change_date = datetime.now()
        
        self._db.commit()
        self._db.refresh(test)
        
        return test
        
    
    def delete_test(self, test_id: int):
        test = self._get_test_or_raise(test_id)
        
        self._db.delete(test)
        self._db.commit()
    
    def _get_test_or_raise(self, test_id: int) -> Test:
        test = self.get_test(test_id)
        if not test:
            raise NoResultFound
        return test