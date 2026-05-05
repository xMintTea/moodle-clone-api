from fastapi import Depends, status, Query, Path
from fastapi.exceptions import HTTPException
from typing import Optional, Annotated
from sqlalchemy.orm import Session

from ..service.section_service import SectionService
from ..database import get_db
from ..models.course import CourseSection, Test, SectionPage
from ..models.user import User
from ..models.context.enums import UserType, Visibility
from ..schemas.sections import SectionCreate, SectionUpdate
from ..security.authorization import get_verified_user
from .courses import get_course_service, CourseService




def get_section_service(session: Session = Depends(get_db)) -> SectionService:
    return SectionService(session)



def list_section_dependency():
    def dependency(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=0, le=1000),
        section_service: SectionService = Depends(get_section_service),
        user: User = Depends(get_verified_user)
    ) -> list[CourseSection]:
        sections = section_service.list_sections(skip, limit)
        
        if user.user_type == UserType.ADMIN:
            return sections
        
        sections = [i for i in sections\
            if (user in i.course.users and i.visibility == Visibility.VISIBLE_EVERYONE) or\
                (user in i.course.users and user not in i.course.students)]
        
        return sections
        
        

    return dependency


def get_section_dependency():
    def dependency(
        section_id: Annotated[int, Path(ge=1)],
        section_service: SectionService = Depends(get_section_service),
        user: User = Depends(get_verified_user)
    ) -> Optional[CourseSection]:
        section = section_service.get_section(section_id)
        
        if section is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_admin = user.user_type == UserType.ADMIN
        can_see = section.visibility == Visibility.VISIBLE_EVERYONE
        have_power = user in section.course.users and user not in section.course.students
        
        if is_admin or can_see or have_power:
            return section
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
    
    return dependency


def create_section_dependency():
    def dependency(
        section_data: SectionCreate,
        section_service: SectionService = Depends(get_section_service),
        course_service: CourseService = Depends(get_course_service),
        user: User = Depends(get_verified_user)
    ) -> CourseSection:
        
        course = course_service.get_course(section_data.course_id)
        
        if course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_admin = user.user_type == UserType.ADMIN
        have_power = user in course.users and user not in course.students
        
        if is_admin or have_power:
            return section_service.create_section(section_data)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return dependency


def update_section_dependency():
    def dependency(
        section_id: Annotated[int, Path(ge=1)],
        section_data: SectionUpdate,
        section_service: SectionService = Depends(get_section_service),
        user: User = Depends(get_verified_user)
    ) -> CourseSection:
        
        section = section_service.get_section(section_id)
        
        if section is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_admin = user.user_type == UserType.ADMIN
        have_power = user in section.course.users and user not in section.course.students
        
        if is_admin or have_power:
            return section_service.update_section(section_id, section_data)
        
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return dependency


def delete_section_dependency():
    def dependency(
        section_id: Annotated[int, Path(ge=1)],
        section_service: SectionService = Depends(get_section_service),
        user: User = Depends(get_verified_user)
    ):
        section = section_service.get_section(section_id)
        
        if section is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_admin = user.user_type == UserType.ADMIN
        have_power = user in section.course.users and user not in section.course.students
        
        if is_admin or have_power:
            section_service.delete_section(section_id)
            
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return dependency
    

def get_pages_in_section_dependency():
    def dependency(
        section_id: Annotated[int, Path(ge=1)],
        section_service: SectionService = Depends(get_section_service),
        user: User = Depends(get_verified_user)
    ) -> list[SectionPage]:
        
        
        pages = section_service.get_pages(section_id)
        
        if user.user_type == UserType.ADMIN:
            return pages
        
        pages = [i for i in pages if i.visibility == Visibility.VISIBLE_EVERYONE or \
            (user in i.section.course.users and user not in i.section.course.students)]
        
        
        return pages

    return dependency

def get_tests_in_section_dependency():
    def dependency(
        section_id: Annotated[int, Path(ge=1)],
        section_service: SectionService = Depends(get_section_service),
        user: User = Depends(get_verified_user)
    ) -> list[Test]:
        
        tests = section_service.get_tests(section_id)
        
        is_admin = user.user_type == UserType.ADMIN
        
        if is_admin:
            return tests
        
        tests = [i for i in tests if i.visibility == Visibility.VISIBLE_EVERYONE or \
            (user in i.section.course.users and user not in i.section.course.students)]
        
        return tests
    
    return dependency