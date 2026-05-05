from fastapi import Depends, status, Query, Path
from fastapi.exceptions import HTTPException
from typing import Optional, Annotated
from sqlalchemy.orm import Session

from ..service.page_service import PageService
from ..service.section_service import SectionService
from ..database import get_db
from ..models.course import SectionPage, SubmittedPage
from ..models.user import User
from ..models.context.enums import Visibility, UserType
from ..schemas.pages import PageCreate, PageUpdate
from ..schemas.submission import PageSubmissionCreate, PageSubmissionUpdate
from ..security.authorization import get_verified_user
from .sections import get_section_service




def get_page_service(session: Session = Depends(get_db)) -> PageService:
    return PageService(session)



def list_pages_dependency():
    def dependency(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=0, le=1000),
        page_service: PageService = Depends(get_page_service),
        user: User = Depends(get_verified_user)
    ) -> list[SectionPage]:
        
        assignments = page_service.list_pages(skip=skip, limit=limit)


        if user.user_type == UserType.ADMIN:
            return assignments
        
        
        assignments = [i for i in assignments\
            if user in i.section.course.users \
                and (i.visibility == Visibility.VISIBLE_EVERYONE or user not in i.section.course.students)]
        
        return assignments

    return dependency


def get_page_dependency():
    def dependency(
        page_id: Annotated[int, Path(ge=1)],
        page_service: PageService = Depends(get_page_service),
        user: User = Depends(get_verified_user)
    ) -> Optional[SectionPage]:
        assignment = page_service.get_page(page_id)
        
        if assignment is None:
            return assignment
        
        user_in_course = user in assignment.section.course.users
        
        can_see = (user.user_type not in assignment.section.course.students and user_in_course) or assignment.visibility == Visibility.VISIBLE_EVERYONE \
            or user.user_type == UserType.ADMIN
            
        if user_in_course or can_see:
           return assignment
       
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return dependency


def create_page_dependency():
    def dependency(
        page_data: PageCreate,
        section_service: SectionService = Depends(get_section_service),
        page_service: PageService = Depends(get_page_service),
        user: User = Depends(get_verified_user)
    ) -> SectionPage:
        
        section = section_service.get_section(page_data.section_id)
        
        if section is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        if user in section.course.teachers or user in section.course.assistants or user.user_type == UserType.ADMIN:
            return page_service.create_page(page_data)

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
    return dependency


def update_page_dependency():
    def dependency(
        page_id: Annotated[int, Path(ge=1)],
        page_data: PageUpdate,
        page_service: PageService = Depends(get_page_service),
        user: User = Depends(get_verified_user)
    ) -> SectionPage:
        
        assignment = page_service.get_page(page_id)
        
        if assignment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_user_on_course = user in assignment.section.course.users
        user_not_student = user is not assignment.section.course.students
        is_admin = user.user_type == UserType.ADMIN
        
        if (is_user_on_course and user_not_student) or is_admin:
            return page_service.update_page(page_id, page_data)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        

    return dependency


def delete_page_dependency():
    def dependency(
        page_id: Annotated[int, Path(ge=1)],
        page_service: PageService = Depends(get_page_service),
        user: User = Depends(get_verified_user)
    ):
        
        assignment = page_service.get_page(page_id)
        
        if assignment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_user_on_course = user in assignment.section.course.users
        user_not_student = user is not assignment.section.course.students
        is_admin = user.user_type == UserType.ADMIN
        
        if (is_user_on_course and user_not_student) or is_admin:
            page_service.delete_page(page_id)
            
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return dependency


def get_page_submissions_dependency():
    def dependency(
        page_id: Annotated[int, Path(ge=1)],
        user_id: Optional[int] = Query(None, ge=1),
        page_service: PageService = Depends(get_page_service),
        user: User = Depends(get_verified_user)
    ) -> list[SubmittedPage]:
        
        assignment = page_service.get_page(page_id)
        
        if assignment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_admin = user.user_type == UserType.ADMIN
        in_course = user in assignment.section.course.users
        student_getting_own_subs = in_course and user.id == user_id
        have_power = in_course and user not in assignment.section.course.students
        
        if student_getting_own_subs or have_power or is_admin:
            return page_service.get_submittions(page_id, user_id)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return dependency


def get_submission_dependency():
    def dependency(
        submittion_id: Annotated[int, Path(ge=1)],
        page_service: PageService = Depends(get_page_service),
        user: User = Depends(get_verified_user)
    ) -> Optional[SubmittedPage]:
        
        submission = page_service.get_submittion(submittion_id)
        
        if submission is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        student_getting_own = user.id == submission.user_id
        is_admin = user.user_type == UserType.ADMIN
        have_power = user in submission.page.section.course.users and user not in submission.page.section.course.students
        
        if student_getting_own or is_admin or have_power:
            return submission
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        

    return dependency


def create_page_submittion_dependency():
    def dependency(
        page_id: Annotated[int, Path(ge=1)],
        page_data: PageSubmissionCreate,
        page_service: PageService = Depends(get_page_service),
        user: User = Depends(get_verified_user)
    ):
        page = page_service.get_page(page_id)
        
        if page is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        if user in page.section.course.users:
            return page_service.create_submittion(page_id, page_data)
        
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return dependency



def update_page_submittion_dependency():
    def dependency(
        submittion_id: Annotated[int, Path(ge=1)],
        submission_data: PageSubmissionUpdate,
        page_service: PageService = Depends(get_page_service),
        user: User = Depends(get_verified_user)
    ) -> SubmittedPage:
        
        sub = page_service.get_submittion(submittion_id)
    
        
        if sub is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        have_power = user in sub.page.section.course.users and user not in sub.page.section.course.students
        is_admin = user.user_type == UserType.ADMIN
        
        if have_power or is_admin:
            return page_service.update_submittion(submittion_id, submission_data)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return dependency


def add_file_to_the_page_dependency():
    def dependency(
        page_id: Annotated[int, Path(ge=1)],
        file_id: Annotated[int, Path(ge=1)],
        page_service: PageService = Depends(get_page_service),
        user: User = Depends(get_verified_user)
    ) -> SectionPage:
        
        page = page_service.get_page(page_id)
        
        if page is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        have_power = user in page.section.course.users and user not in page.section.course.students
        is_admin = user.user_type == UserType.ADMIN
        
        if have_power or is_admin:
            return page_service.add_file_to_page(page_id, file_id)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return dependency


def add_file_to_the_submission_dependency():
    def dependency(
        submittion_id: Annotated[int, Path(ge=1)],
        file_id: Annotated[int, Path(ge=1)],
        page_service: PageService = Depends(get_page_service),
        user: User = Depends(get_verified_user)
    ) -> SubmittedPage:
        
        sub = page_service.get_submittion(submittion_id)
        
        if sub is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        if user.id == sub.user_id:
            return page_service.add_file_to_submittion(submittion_id, file_id)
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return dependency

