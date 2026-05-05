from fastapi.exceptions import HTTPException
from fastapi import status

from ...models.course import CourseUser, Course
from ...models.user import User
from ...models.context.enums import UserType, UserStatus, Visibility
from ...schemas.course_user import CreateCourseUser



class AddUserToCoursePolicy():
    def __init__(self, authed_user: User, data: CreateCourseUser, course: Course, secret: str) -> None:
        
        if course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        is_admin = authed_user.user_type == UserType.ADMIN
        is_same_user = authed_user.id == data.user_id
        is_active = authed_user.user_status == UserStatus.ACTIVE
        can_see_course = course.visibility == Visibility.VISIBLE_EVERYONE
        is_secret_matched = course.secret is None or course.secret == secret
        
        case1 = is_admin and is_active
        case2 = is_active and can_see_course and is_same_user and is_secret_matched
        
        allow = any([case1, case2])
        
        if not allow:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

class UpdateCourseUserPolicy:
    def __init__(self,authed_user: User,other_user_id: int, record: CourseUser) -> None:
        record_exists = record is not None
        is_teacher = authed_user in record.course.teachers
        is_admin = authed_user.user_type == UserType.ADMIN
        changing_other_user = authed_user.id != other_user_id
        not_banned = authed_user.user_status == UserStatus.ACTIVE
        
        case1 = record_exists and is_teacher and changing_other_user
        case2 = record_exists and not is_teacher and not changing_other_user
        case3 = is_admin
        
        allowed = any([case1, case2, case3])
        allowed = allowed and not_banned
        
        if not allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        

