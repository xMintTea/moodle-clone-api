from fastapi import Depends, status, Query, Path
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from typing import Optional, Annotated
from sqlalchemy.orm import Session
import json

from ..service.test_service import TestService
from ..database import get_db
from ..models.course import Test
from ..models.user import User
from ..models.context.enums import UserType, Visibility
from ..schemas.tests import TestCreate, TestUpdate, TestResponse
from ..schemas.test_answers import AnswerCreate
from ..security.authorization import get_verified_user
from .sections import SectionService, get_section_service


def get_test_service(session: Session = Depends(get_db)) -> TestService:
    return TestService(session)



def list_tests_dependency():
    def dependency(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        test_service: TestService = Depends(get_test_service),
        user: User = Depends(get_verified_user)
    ) -> list[Test]:
        
        tests =test_service.list_tests(skip=skip, limit=limit)
        
        if user.user_type == UserType.ADMIN:
            return tests
        
        tests = [i for i in tests if i.visibility == Visibility.VISIBLE_EVERYONE or \
            (user in i.section.course.users and user not in i.section.course.students)]
        
        return tests
        
    
    return dependency


def get_test_dependency():
    def dependency(
        test_id: Annotated[int, Path(ge=1)],
        test_service: TestService = Depends(get_test_service),
        user: User = Depends(get_verified_user)
    ) -> Optional[Test]:
        test = test_service.get_test(test_id)
        
        if test is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_admin = user.user_type == UserType.ADMIN
        can_see = test.visibility == Visibility.VISIBLE_EVERYONE
        have_power = user in test.section.course.users and user not in test.section.course.students
        
        if can_see and not have_power:
            raw_content = test.content

            if raw_content is None:
                return test
            

            if isinstance(raw_content, str):
                content_list = json.loads(raw_content)
                was_string = True
            else:
                content_list = raw_content
                was_string = False
                
                
            for q in content_list:
                if q.get("type") == "write_answer":
                    q["answer"] = ""
                elif "answers" in q:
                    q["answers"] = [""] if isinstance(q["answers"], list) else {"":""}
                    
                    
            if was_string:
                test.content = json.dumps(content_list, indent=2, ensure_ascii=False)
            else:
                test.content = content_list

            return test
            
            
            
        
        if is_admin or can_see or have_power:
            return test
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)        
    
    return dependency


def create_test_dependency():
    def dependency(
        test_data: TestCreate,
        test_service: TestService = Depends(get_test_service),
        section_service: SectionService = Depends(get_section_service),
        user: User = Depends(get_verified_user)
    ) -> Test:
        
        section = section_service.get_section(test_data.section_id)
        
        if section is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_admin = user.user_type == UserType.ADMIN
        have_power = user in section.course.users and user not in section.course.students
        
        if is_admin or have_power:
            return test_service.create_test(test_data)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return dependency


def update_test_dependency():
    def dependency(
        test_id: Annotated[int, Path(ge=1)],
        test_data: TestUpdate,
        test_service: TestService = Depends(get_test_service),
        user: User = Depends(get_verified_user)
    ) -> Test:
        
        test = test_service.get_test(test_id)
        
        if test is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_admin = user.user_type == UserType.ADMIN
        have_power = user in test.section.course.users and user not in test.section.course.students
        
        if is_admin or have_power:
            return test_service.update_test(test_id, test_data)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return dependency


def delete_test_dependency():
    def dependency(
        test_id: Annotated[int, Path(ge=1)],
        test_service: TestService = Depends(get_test_service),
        user: User = Depends(get_verified_user)
    ):
        
        test = test_service.get_test(test_id)
        
        if test is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        
        is_admin = user.user_type == UserType.ADMIN
        have_power = user in test.section.course.users and user not in test.section.course.students
        
        if is_admin or have_power:
            test_service.delete_test(test_id)
            
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
        
    return dependency


def get_attempts_dependency():
    def dependency(
        test_id: Annotated[int, Path(ge=1)],
        user_id: int = Query(None, ge=1),
        test_service: TestService = Depends(get_test_service),
        user: User = Depends(get_verified_user)
        ):
        
        can_access = user.user_type != UserType.DEFAULT or user.id == user_id
        
        if can_access:
            return test_service.get_attempts(test_id, user_id)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
    return dependency


def create_attempt_dependency():
    def dependency(
        test_id: Annotated[int, Path(ge=1)],
        attempt_data: AnswerCreate,
        test_service: TestService = Depends(get_test_service),
        user: User = Depends(get_verified_user)
    ):
        same_user = user.id == attempt_data.user_id
        test_service.create_attempt(test_id, attempt_data)
    
    return dependency