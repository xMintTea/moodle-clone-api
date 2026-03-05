from fastapi import Depends, status, Query
from fastapi.routing import APIRouter
from typing import Optional
from sqlalchemy.orm import Session

from ...service.course_service import CourseService
from ...database import get_db
from ...models.course import Course
from ...schemas.course import CourseCreate, CourseUpdate, CourseResponce

router = APIRouter(prefix="/courses", tags=["Courses"])


def get_course_service(session: Session = Depends(get_db)) -> CourseService:
    return CourseService(session)

@router.get("/", response_model=list[CourseResponce])
def list_courses(
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
