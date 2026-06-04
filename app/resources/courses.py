from fastapi import Depends, status, Query, Path
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from typing import Optional, Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from ..service.course_service import CourseService
from ..service.course_user_service import CourseUserService
from ..database import get_db
from ..models.course import Course, CourseUser
from ..models.user import User
from ..models.context.enums import UserType, Visibility, CourseAccessLevel, CourseAccessStatus
from ..schemas.course import CourseCreate, CourseUpdate, CourseResponce
from ..schemas.course_user import CreateCourseUser, UpdateCourseUser, CourseUserResponse
from ..security.authorization import get_verified_user
from ..security.policies.course_policies import AddUserToCoursePolicy, UpdateCourseUserPolicy


def get_course_service(session: Session = Depends(get_db)) -> CourseService:
    return CourseService(session)

def get_course_user_service(session: Session = Depends(get_db)) -> CourseUserService:
    return CourseUserService(session)



def get_course_list_dependency():
    def dependency(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        course_service: CourseService = Depends(get_course_service),
        user: User = Depends(get_verified_user)
    ) -> list[Course]:
        
        
        
        course_list = course_service.list_courses(skip, limit)
        
        if user.user_type == UserType.DEFAULT:
            course_list = [i for i in course_list\
                if i.visibility == Visibility.VISIBLE_EVERYONE or user in i.users]
            
        if user.user_type == UserType.REDACTOR:
            course_list = [i for i in course_list\
                if i.visibility == Visibility.VISIBLE_EVERYONE\
                or (user in i.teachers and i.visibility == Visibility.VISIBLE_TO_CREATOR)]
            
        
        
        return course_list

    return dependency



def get_course_dependency():
    def dependency(
        course_id: int,
        course_service: CourseService = Depends(get_course_service),
        user: User = Depends(get_verified_user)
    ) -> Optional[Course]:
        
        course = course_service.get_course(course_id)
        
        if course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        if course.visibility == Visibility.VISIBLE_EVERYONE:
            return course
        
        if course.visibility == Visibility.VISIBLE_TO_CREATOR and user in course.teachers:
            return course
        
        if user.user_type == UserType.ADMIN:
            return course
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
    
    return dependency


def create_course_dependency():
    def dependency(
        course_data: CourseCreate,
        course_user_service: CourseUserService = Depends(get_course_user_service),
        course_service: CourseService = Depends(get_course_service),
        user: User = Depends(get_verified_user)
    ) -> Course:
        
        if user.user_type == UserType.DEFAULT:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
        course = course_service.create_course(course_data)
        
        data = CreateCourseUser(access_level=CourseAccessLevel.TEACHER, access_status=CourseAccessStatus.GRANTED, user_id=user.id)
        
        course_user_service.add_record(course.id, data)
        
        return course
        
    
    return dependency


def update_course_dependency():
    def dependency(
        course_id: int,
        course_data: CourseUpdate,
        course_service: CourseService = Depends(get_course_service),
        user: User = Depends(get_verified_user)
    ) -> Course:
        
        course = course_service.get_course(course_id)
        
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_teacher = user in course.teachers
        admin = user.user_type == UserType.ADMIN
        
        if not (is_teacher or admin):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
        return course_service.update_course(course_id, course_data)
    
    return dependency


def delete_course_dependency():
    def dependency(
        course_id: int,
        course_service: CourseService = Depends(get_course_service),
        user: User = Depends(get_verified_user)
    ):
        
        course = course_service.get_course(course_id)
        
        if course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        if user.user_type == UserType.DEFAULT:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
        can_do_it = user in course.teachers or user.user_type == UserType.ADMIN
        
        if not can_do_it:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
        course_service.delete_course(course_id)
        
    return dependency


def get_course_users_dependency():
    def dependency(
        course_id: int,
        course_user_service: CourseUserService = Depends(get_course_user_service),
        course_service: CourseService = Depends(get_course_service),
        user: User = Depends(get_verified_user)
    ) -> list[CourseUser]:
        
        course = course_service.get_course(course_id)
        
        if course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        can_do = user in course.assistants or user in course.teachers
        admin = user.user_type == UserType.ADMIN
        
        if not (can_do or admin):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            
        
        return course_user_service.list_records_in_course(course_id)
    
    return dependency


def add_user_to_the_course_dependency():
    def dependency(
        course_id: Annotated[int, Path(..., ge=1)],
        courseuser_data: CreateCourseUser,
        secret: Optional[str] = Query(default=None),
        course_service: CourseService = Depends(get_course_service),
        course_user_service: CourseUserService = Depends(get_course_user_service),
        user: User = Depends(get_verified_user)
    ) -> CourseUser:
        
        course = course_service.get_course(course_id)
        
        AddUserToCoursePolicy(user, courseuser_data, course, secret) #type: ignore
        
        return course_user_service.add_record(course_id, courseuser_data)
    
    return dependency


def update_user_on_the_course_dependency():
    def dependency(
        course_id: int,
        user_id: int,
        course_user_data: UpdateCourseUser,
        course_service: CourseService = Depends(get_course_service),
        course_user_service: CourseUserService = Depends(get_course_user_service),
        authed_user: User = Depends(get_verified_user)
    ) -> Course:
        
        
        record = course_user_service.find_record(course_id, user_id)

        UpdateCourseUserPolicy(authed_user, user_id, record) #type: ignore
        
        course_user_service.update_record(record.id, course_user_data)  #type: ignore
        
        return record.course  #type: ignore
        
    return dependency


def delete_user_from_the_course_dependency():
    def dependency(
        course_id: int,
        user_id: int,
        course_service: CourseService = Depends(get_course_service),
        course_user_service: CourseUserService = Depends(get_course_user_service),
        user: User = Depends(get_verified_user)
    ):
        
        course = course_service.get_course(course_id)
        
        if course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        student_trying_leave = user.id == user_id and user in course.students
        
        can_do_it = user in course.teachers or user.user_type == UserType.ADMIN
        
        case1 = student_trying_leave
        case2 = can_do_it and not student_trying_leave
        
        if not (case1 or case2):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


        record = course_user_service.find_record(course_id, user_id)
        
        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        course_user_service.delete_record(record.id)
        
        
    return dependency

