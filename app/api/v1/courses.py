from fastapi import Depends, status, Query
from fastapi.routing import APIRouter
from typing import Optional
from sqlalchemy.orm import Session

from ...service.course_service import CourseService
from ...service.course_user_service import CourseUserService
from ...database import get_db
from ...models.course import Course, CourseUser
from ...schemas.course import CourseCreate, CourseUpdate, CourseResponce
from ...schemas.course_user import CreateCourseUser, UpdateCourseUser, CourseUserResponse

router = APIRouter(prefix="/courses", tags=["Courses"])


def get_course_service(session: Session = Depends(get_db)) -> CourseService:
    return CourseService(session)


def get_course_user_service(session: Session = Depends(get_db)) -> CourseUserService:
    return CourseUserService(session)


@router.get("/", response_model=list[CourseResponce])
async def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    course_service: CourseService = Depends(get_course_service)
) -> list[Course]:
    return course_service.list_courses(skip, limit)


@router.get("/{course_id}", response_model=CourseResponce)
def get_course(
    course_id: int,
    course_service: CourseService = Depends(get_course_service)
) -> Optional[Course]:
    return course_service.get_course(course_id)

@router.post("/", response_model=CourseResponce)
def create_course(
    course_data: CourseCreate,
    course_service: CourseService = Depends(get_course_service)
) -> Course:
    return course_service.create_course(course_data)

@router.put("/{course_id}",response_model=CourseResponce)
def update_course(
    course_id: int,
    course_data: CourseUpdate,
    course_service: CourseService = Depends(get_course_service)
) -> Course:
    return course_service.update_course(course_id, course_data)

@router.delete("/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT
    )
def delete_course(
    course_id: int,
    course_service: CourseService = Depends(get_course_service)
):
    course_service.delete_course(course_id)


@router.get("/{course_id}/members/", response_model=list[CourseUserResponse])
def get_course_users(
    course_id: int,
    course_user_service: CourseUserService = Depends(get_course_user_service)   
) -> list[CourseUser]:
    return course_user_service.list_records_in_course(course_id)


@router.post("/{course_id}/members/", response_model=CourseUserResponse)
def add_user_to_the_course(
    course_id: int,
    courseuser_data: CreateCourseUser,
    course_user_service: CourseUserService = Depends(get_course_user_service)   
) -> CourseUser:
    return course_user_service.add_record(course_id, courseuser_data)
    

@router.put("/{course_id}/members/{user_id}", response_model=CourseUserResponse)
def update_user_on_the_course(
    course_id: int,
    user_id: int,
    courseuser_data: UpdateCourseUser,
    course_service: CourseService = Depends(get_course_service)   
) -> Course:
    ...
    
@router.delete("/{course_id}/members/{user_id}")
def delete_user_from_the_course(
    course_id: int,
    user_id: int,
    course_service: CourseService = Depends(get_course_service)   
):
    ...
    
@router.get("/{course_id}/admins")
def get_course_admins(
    course_id: int
):
    ...
    
@router.get("/{course_id}/teacher")
def get_course_teachers(
    course_id: int
):
    ...