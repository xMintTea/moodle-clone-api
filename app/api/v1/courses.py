from fastapi import Depends, status, Query
from fastapi.routing import APIRouter
from typing import Optional

from ...models.course import Course, CourseUser
from ...schemas.course import CourseResponce
from ...schemas.course_user import CourseUserResponse
from ...resources.courses import(
    get_course_list_dependency,
    get_course_dependency,
    create_course_dependency,
    update_course_dependency,
    delete_course_dependency,
    get_course_users_dependency,
    add_user_to_the_course_dependency,
    update_user_on_the_course_dependency,
    delete_user_from_the_course_dependency
    )

router = APIRouter(prefix="/courses", tags=["Courses"])




@router.get("/", response_model=list[CourseResponce])
async def list_courses(
    course_list: list[Course] = Depends(get_course_list_dependency())
) -> list[Course]:
    return course_list


@router.get("/{course_id}", response_model=CourseResponce)
def get_course(
    course: Optional[Course] = Depends(get_course_dependency())
) -> Optional[Course]:
    return course

@router.post("/", response_model=CourseResponce, status_code=status.HTTP_201_CREATED)
def create_course(
    course: Course = Depends(create_course_dependency())
) -> Course:
    return course

@router.put("/{course_id}",response_model=CourseResponce)
def update_course(
    course: Course = Depends(update_course_dependency())
) -> Course:
    return course

@router.delete("/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT
    )
def delete_course(
    _ = Depends(delete_course_dependency())
):
    ...


@router.get("/{course_id}/members/", response_model=list[CourseUserResponse])
def get_course_users(
    course_users: list[CourseUser] = Depends(get_course_users_dependency())
) -> list[CourseUser]:
    return course_users


@router.post(
    "/{course_id}/members/",
    response_model=CourseUserResponse,
    status_code=status.HTTP_202_ACCEPTED)
def add_user_to_the_course(
    course_user: CourseUser = Depends(add_user_to_the_course_dependency())
) -> CourseUser:
    return course_user
    

@router.put(
    "/{course_id}/members/{user_id}",
    response_model=CourseUserResponse,
    status_code=status.HTTP_202_ACCEPTED)
def update_user_on_the_course(
    course: Course = Depends(update_user_on_the_course_dependency())
) -> Course:
    return course


@router.delete("/{course_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_from_the_course(
    _ = Depends(delete_user_from_the_course_dependency())
):
    ...